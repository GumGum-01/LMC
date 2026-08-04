import sys, re, cairosvg
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import figures

# cairosvg's CSS support is unreliable -> inline the class styles as attributes
STY = {
 "bd":'stroke="#161A19" fill="none" stroke-linecap="round"',
 "br":'stroke="#161A19"',
 "at":'font-family="Helvetica" fill="#161A19"',
 "mid":'text-anchor="middle"',
 "pc":'fill="none" stroke="#A8501E" stroke-width="1.3"',
 "ox":'fill="#0F5B67" font-weight="600"',
 "hy":'fill="#5E6A68"',
 "nm":'fill="#8A9694" font-family="monospace"',
 "nmx":'fill="#161A19" font-weight="700"',
 "cp":'fill="#5E6A68" font-family="Helvetica"',
 "em":'fill="#A8501E" font-weight="600"',
 "nu":'fill="#0F5B67" font-weight="600"',
 "rg":'fill="#B6BFBD" font-weight="700"',
 "sm":'fill="#6B7674"',
 "ar":'stroke="#A8501E" fill="none" stroke-width="1.9"',
 "hdf":'fill="#A8501E"',
 "rx":'stroke="#161A19" stroke-width="1.5"',
 "rhf":'fill="#161A19"',
 "nb":'fill="#A8501E" stroke="none"',
 "nn":'fill="#F2F4F3" font-weight="700" font-family="monospace"',
 "fl":'fill="#161A19" font-weight="600"',
}
def inline(m):
    attrs = {}
    for c in m.group(1).split():
        for k, v in re.findall(r'([a-z-]+)="([^"]*)"', STY.get(c, "")):
            attrs[k] = v
    return " ".join(f'{k}="{v}"' for k, v in attrs.items())

out = Path("/tmp/claude-0/-home-user-LMC/63e349b2-56f4-5c29-882e-0c28430b0e50/scratchpad/proof")
out.mkdir(parents=True, exist_ok=True)
for k in (sys.argv[1:] or list(figures.FIGS)):
    s = re.sub(r'class="([^"]*)"', inline, figures.FIGS[k])
    s = s.replace('&#8722;', '-')  # cairosvg hat keine Minus-Glyphe
    s = s.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ')
    cairosvg.svg2png(bytestring=s.encode(), write_to=str(out/f"{k}.png"),
                     scale=2.2, background_color="#F2F4F3")
    print("wrote", k)
