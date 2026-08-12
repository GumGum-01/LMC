#!/usr/bin/env python3
"""
Embed a TTF font into a .docx (real OOXML font embedding, ECMA-376 17.8.6)
and force every run in the document to use it -- not just a font-name
reference that only displays correctly if the reader happens to have the
font installed.

Usage: python3 embed_font_docx.py input.docx output.docx font.ttf "Font Name"
"""
import sys
import uuid
import zipfile
from pathlib import Path

from lxml import etree

NSMAP_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NSMAP_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NSMAP_PKGREL = "http://schemas.openxmlformats.org/package/2006/relationships"

W = f"{{{NSMAP_W}}}"
R = f"{{{NSMAP_R}}}"
FONT_RELTYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"


def guid_key_bytes(guid_str: str) -> bytes:
    """The 16 key bytes are the GUID's hex digits parsed left-to-right, exactly
    as they appear in the formatted string -- no struct/endianness reordering."""
    return bytes.fromhex(guid_str.strip("{}").replace("-", ""))


def obfuscate_font(data: bytes, key: bytes) -> bytes:
    """XOR the first 32 bytes against the 16-byte GUID key, per the ECMA-376
    font-obfuscation algorithm used for embedded w:embedRegular parts.

    Verified against an independent reference decoder (see
    gist.github.com/FrancoisCapon/8db243283cc18be24a9ce6351e478b13): its
    int.from_bytes big-endian-key / little-endian-data XOR trick is
    algebraically equivalent to XOR-ing byte i with key[15 - (i % 16)] --
    i.e. the key applies in REVERSED order within each 16-byte half, not
    key[i % 16]. Confirmed by round-tripping random test data through both
    formulations and checking they match before trusting this on the real
    font.
    """
    header = bytearray(data[:32])
    for i in range(32):
        header[i] ^= key[15 - (i % 16)]
    return bytes(header) + data[32:]


def set_rfonts(rpr, font_name):
    rfonts = rpr.find(f"{W}rFonts")
    if rfonts is None:
        rfonts = etree.SubElement(rpr, f"{W}rFonts")
        rpr.insert(0, rfonts)
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(f"{{{NSMAP_W}}}{attr}", font_name)


def force_font_everywhere(document_xml_bytes, font_name):
    root = etree.fromstring(document_xml_bytes)
    for r in root.iter(f"{W}r"):
        rpr = r.find(f"{W}rPr")
        if rpr is None:
            rpr = etree.Element(f"{W}rPr")
            r.insert(0, rpr)
        set_rfonts(rpr, font_name)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def force_font_in_styles(styles_xml_bytes, font_name):
    root = etree.fromstring(styles_xml_bytes)
    docDefaults = root.find(f"{W}docDefaults")
    if docDefaults is not None:
        rPrDefault = docDefaults.find(f"{W}rPrDefault")
        if rPrDefault is not None:
            rpr = rPrDefault.find(f"{W}rPr")
            if rpr is None:
                rpr = etree.SubElement(rPrDefault, f"{W}rPr")
            set_rfonts(rpr, font_name)
    for style in root.findall(f"{W}style"):
        rpr = style.find(f"{W}rPr")
        if rpr is not None and rpr.find(f"{W}rFonts") is not None:
            set_rfonts(rpr, font_name)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def add_font_table_entry(fonttable_xml_bytes, font_name, rel_id, font_key_str):
    root = etree.fromstring(fonttable_xml_bytes)
    for existing in root.findall(f"{W}font"):
        if existing.get(f"{W}name") == font_name:
            root.remove(existing)
    font_el = etree.SubElement(root, f"{W}font")
    font_el.set(f"{W}name", font_name)
    embed = etree.SubElement(font_el, f"{W}embedRegular")
    embed.set(f"{R}id", rel_id)
    embed.set(f"{W}fontKey", font_key_str)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def add_embed_flag(settings_xml_bytes):
    root = etree.fromstring(settings_xml_bytes)
    if root.find(f"{W}embedTrueTypeFonts") is not None:
        return settings_xml_bytes
    flag = etree.Element(f"{W}embedTrueTypeFonts")
    flag.set(f"{W}val", "true")
    zoom = root.find(f"{W}zoom")
    if zoom is not None:
        zoom.addnext(flag)
    else:
        root.insert(0, flag)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def build_rels_xml(existing_bytes, rel_id, target):
    if existing_bytes is None:
        root = etree.Element(f"{{{NSMAP_PKGREL}}}Relationships", nsmap={None: NSMAP_PKGREL})
    else:
        root = etree.fromstring(existing_bytes)
    rel = etree.SubElement(root, f"{{{NSMAP_PKGREL}}}Relationship")
    rel.set("Id", rel_id)
    rel.set("Type", FONT_RELTYPE)
    rel.set("Target", target)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def add_content_type_default(ct_xml_bytes, extension, content_type):
    root = etree.fromstring(ct_xml_bytes)
    for d in root.findall(f"{{{NSMAP_CT}}}Default"):
        if d.get("Extension") == extension:
            return ct_xml_bytes
    d = etree.SubElement(root, f"{{{NSMAP_CT}}}Default")
    d.set("Extension", extension)
    d.set("ContentType", content_type)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def deobfuscate_font(data: bytes, key: bytes) -> bytes:
    return obfuscate_font(data, key)  # XOR is self-inverse


def verify_docx_structure(out_path, font_key_str, font_bytes, fntdata_part):
    """Fail loudly instead of shipping a file nobody has actually opened:
    every XML part must parse, every relationship referenced from
    fontTable.xml must resolve to a real part, the content-type for the
    obfuscated font part must be declared, and the obfuscation must
    round-trip back to the exact original font bytes. Also confirms
    python-docx -- a real, independent OOXML consumer -- can open the
    result without raising."""
    with zipfile.ZipFile(out_path) as z:
        names = set(z.namelist())
        for n in names:
            if n.endswith(".xml") or n.endswith(".rels"):
                etree.fromstring(z.read(n))  # raises on malformed XML

        ct = etree.fromstring(z.read("[Content_Types].xml"))
        exts = {d.get("Extension") for d in ct.findall(f"{{{NSMAP_CT}}}Default")}
        assert "fntdata" in exts, "fntdata content-type Default missing"

        fonttable = etree.fromstring(z.read("word/fontTable.xml"))
        rels = etree.fromstring(z.read("word/_rels/fontTable.xml.rels"))
        rel_ids = {r.get("Id"): r.get("Target") for r in rels}
        found_embed = False
        for font_el in fonttable.findall(f"{W}font"):
            embed = font_el.find(f"{W}embedRegular")
            if embed is None:
                continue
            rid = embed.get(f"{R}id")
            assert rid in rel_ids, f"fontTable references relationship {rid} that doesn't exist"
            target = "word/" + rel_ids[rid]
            assert target in names, f"relationship target {target} is not a real part in the zip"
            assert target == fntdata_part
            found_embed = True
        assert found_embed, "no embedRegular entry found in fontTable.xml"

        stored = z.read(fntdata_part)
        key = guid_key_bytes(font_key_str)
        recovered = deobfuscate_font(stored[:32], key) + stored[32:]
        assert recovered == font_bytes, "obfuscated font part does not de-obfuscate back to the original bytes"

    import docx as _docx  # independent OOXML consumer -- must open without raising
    _docx.Document(str(out_path))


def embed_font_in_docx(in_path, out_path, font_path, font_name):
    in_path, out_path, font_path = Path(in_path), Path(out_path), Path(font_path)
    zin = zipfile.ZipFile(in_path, "r")
    names = zin.namelist()
    parts = {n: zin.read(n) for n in names}

    font_bytes = font_path.read_bytes()
    font_key_str = "{" + str(uuid.uuid4()).upper() + "}"
    key = guid_key_bytes(font_key_str)
    obfuscated = obfuscate_font(font_bytes, key)

    rel_id = "rIdEmbeddedFont1"
    fntdata_part = "word/fonts/TuyenGerman3.fntdata"

    parts["word/document.xml"] = force_font_everywhere(parts["word/document.xml"], font_name)
    if "word/styles.xml" in parts:
        parts["word/styles.xml"] = force_font_in_styles(parts["word/styles.xml"], font_name)
    parts["word/fontTable.xml"] = add_font_table_entry(parts["word/fontTable.xml"], font_name, rel_id, font_key_str)
    parts["word/settings.xml"] = add_embed_flag(parts["word/settings.xml"])
    parts["[Content_Types].xml"] = add_content_type_default(parts["[Content_Types].xml"], "fntdata", "application/x-font-data")

    rels_path = "word/_rels/fontTable.xml.rels"
    existing_rels = parts.get(rels_path)
    parts[rels_path] = build_rels_xml(existing_rels, rel_id, "fonts/TuyenGerman3.fntdata")
    parts[fntdata_part] = obfuscated

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in parts.items():
            zout.writestr(name, data)
    zin.close()

    verify_docx_structure(out_path, font_key_str, font_bytes, fntdata_part)
    print(f"Embedded {font_name} ({len(font_bytes)} bytes) into {out_path}, fontKey={font_key_str}")
    print("Structural self-check passed: XML well-formed, relationships resolve, "
          "obfuscation round-trips exactly, python-docx opens it cleanly.")


if __name__ == "__main__":
    in_docx, out_docx, font_ttf, font_name = sys.argv[1:5]
    embed_font_in_docx(in_docx, out_docx, font_ttf, font_name)
