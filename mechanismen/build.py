#!/usr/bin/env python3
"""Baut mechanismus.html aus den generierten SVGs (figures.py) und dem Text."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from figures import FIGS  # noqa: E402

HERE = Path(__file__).parent


def fig(key, caption):
    return (f'<figure><div class="scroll">{FIGS[key]}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


def pf(*items):
    li = "".join(f'<li><span class="pf">{n}</span><span>{t}</span></li>'
                 for n, t in items)
    return f'<ol class="pfeile">{li}</ol>'


def merk(text):
    return f'<aside class="merk"><p><span class="mk">Merkbild</span>{text}</p></aside>'


CSS = """
:root{
  --paper:#EEF1F0; --card:#F6F8F7; --ink:#12181A; --muted:#59696A;
  --rule:#CBD5D2; --copper:#B4531D; --copper-soft:#F0E0D5; --petrol:#0E5B66;
  --sans:Helvetica,Arial,"Helvetica Neue",system-ui,sans-serif;
  --disp:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --serif:Charter,"Bitstream Charter","Iowan Old Style","Source Serif 4",Georgia,serif;
  --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){
  :root{--paper:#0D1315; --card:#131B1D; --ink:#E3EAE8; --muted:#8DA09F;
        --rule:#22302F; --copper:#E28A4C; --copper-soft:#33211591; --petrol:#5FBACB;}
}
:root[data-theme="dark"]{--paper:#0D1315; --card:#131B1D; --ink:#E3EAE8; --muted:#8DA09F;
  --rule:#22302F; --copper:#E28A4C; --copper-soft:#33211591; --petrol:#5FBACB;}
:root[data-theme="light"]{--paper:#EEF1F0; --card:#F6F8F7; --ink:#12181A; --muted:#59696A;
  --rule:#CBD5D2; --copper:#B4531D; --copper-soft:#F0E0D5; --petrol:#0E5B66;}

*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--serif);font-size:17px;line-height:1.62;
  -webkit-font-smoothing:antialiased}
.wrap{max-width:900px;margin:0 auto;padding:0 24px 96px}
p{margin:0 0 1em;max-width:66ch}
b,strong{font-weight:700}

/* ---------- Kopf ---------- */
header{padding:72px 0 40px;border-bottom:1px solid var(--rule)}
.kicker{font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--copper);margin:0 0 18px}
h1{font-family:var(--disp);font-size:clamp(30px,5.2vw,50px);line-height:1.05;
  letter-spacing:-.022em;font-weight:800;margin:0 0 18px;text-wrap:balance;max-width:20ch}
.stand{font-size:19px;color:var(--muted);max-width:60ch;margin:0}

/* ---------- Substrat-Tabelle ---------- */
.tbl{width:100%;border-collapse:collapse;margin:28px 0 8px;font-family:var(--sans);
  font-size:14.5px;font-variant-numeric:tabular-nums}
.tbl th{text-align:left;font-family:var(--mono);font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);font-weight:400;
  padding:0 14px 8px 0;border-bottom:1px solid var(--rule)}
.tbl td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule);vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.tbl td:first-child{font-weight:700}

/* ---------- Schritte ---------- */
.step{padding:52px 0;border-bottom:1px solid var(--rule)}
.step:last-of-type{border-bottom:none}
.eyebrow{font-family:var(--mono);font-size:11.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--copper);margin:0 0 10px}
h2{font-family:var(--disp);font-size:clamp(21px,2.9vw,27px);line-height:1.22;
  letter-spacing:-.015em;font-weight:750;margin:0 0 16px;text-wrap:balance;max-width:26ch}
h3{font-family:var(--disp);font-size:15px;letter-spacing:.005em;font-weight:700;
  margin:30px 0 10px}

/* ---------- Figuren ---------- */
figure{margin:26px 0 22px;background:var(--card);border:1px solid var(--rule);
  border-radius:2px;padding:22px 20px 16px}
.scroll{overflow-x:auto;overflow-y:hidden;display:flex;justify-content:center}
figure svg{display:block;width:100%;height:auto;
  max-width:calc(var(--w) * 1.85px);min-width:calc(var(--w) * 0.80px)}
figcaption{font-family:var(--sans);font-size:13px;line-height:1.5;color:var(--muted);
  margin-top:16px;padding-top:12px;border-top:1px solid var(--rule);max-width:78ch}

/* Strukturformeln */
.bd{stroke:var(--ink);fill:none;stroke-linecap:round}
.bg{stroke:var(--copper)}
.wg{fill:var(--ink);stroke:none}
.at{font-family:var(--sans)}
.mid{text-anchor:middle}
.hl{paint-order:stroke;stroke:var(--card);stroke-width:3.6px;stroke-linejoin:round}
.ox{fill:var(--petrol);font-weight:600}
.hy{fill:var(--muted)}
.nm{fill:var(--muted);opacity:.75;font-family:var(--mono)}
.nmx{fill:var(--ink);font-weight:700}
.fl{fill:var(--ink);font-weight:700}
.cp{fill:var(--muted)}
.sm{fill:var(--muted)}
.rg{fill:var(--rule);font-weight:700}
.em{fill:var(--copper);font-weight:700}
.nu{fill:var(--petrol);font-weight:700}
.bgl{fill:var(--copper);font-weight:700}
.ar{stroke:var(--copper);fill:none;stroke-width:1.9}
.dsh{stroke-dasharray:5 4}
.hdf{fill:var(--copper)}
.rx{stroke:var(--ink);stroke-width:1.5;fill:none}
.rhf{fill:var(--ink)}
.nb{fill:var(--copper);stroke:none}
.nn{fill:var(--card);font-weight:700;font-family:var(--mono)}
.pc{fill:none;stroke:var(--copper);stroke-width:1.3}

/* ---------- Pfeil-Listen ---------- */
.pfeile{list-style:none;margin:22px 0;padding:0;display:flex;flex-direction:column;gap:11px}
.pfeile li{display:flex;gap:13px;align-items:baseline;max-width:70ch}
.pf{flex:0 0 auto;display:inline-grid;place-items:center;width:22px;height:22px;
  border-radius:50%;background:var(--copper);color:var(--card);
  font-family:var(--mono);font-size:11.5px;font-weight:700;
  transform:translateY(3px)}

/* ---------- Merkbild ---------- */
.merk{margin:24px 0 0;padding:16px 18px;background:var(--copper-soft);
  border-left:2px solid var(--copper);border-radius:0 2px 2px 0}
.merk p{margin:0;font-size:16px;max-width:64ch}
.mk{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--copper);display:block;margin-bottom:5px}

/* ---------- Hinweiskasten ---------- */
.note{margin:26px 0;padding:16px 18px;border:1px solid var(--rule);border-radius:2px}
.note p{margin:0 0 .6em;font-size:15.5px;color:var(--muted)}
.note p:last-child{margin:0}
.note .mk{color:var(--petrol)}

/* ---------- Antwortkasten ---------- */
.answer{margin:44px 0 0;padding:26px 26px 20px;background:var(--card);
  border:1px solid var(--rule);border-top:3px solid var(--copper);border-radius:2px}
.answer h2{margin-top:0}
.answer ol{margin:0;padding-left:1.3em}
.answer li{margin-bottom:.7em;max-width:62ch}

code{font-family:var(--mono);font-size:.88em;background:var(--card);
  border:1px solid var(--rule);border-radius:2px;padding:1px 5px}
em.pos{font-family:var(--mono);font-style:normal;font-size:.9em;color:var(--petrol)}
footer{padding:40px 0 0;color:var(--muted);font-family:var(--sans);font-size:13px}
"""


BODY = f"""
<div class="wrap">

<header>
  <p class="kicker">LMC StEx · Lebensmittelchemie der Polyphenole</p>
  <h1>Oxidative Kupplung: vom Catechin zum Benzotropolon</h1>
  <p class="stand">Jeder Schritt einzeln gezeichnet, jeder Pfeil einzeln begründet —
  von der Polyphenoloxidase bis zu der Frage, warum das Endprodukt kupferrot ist.</p>

  <table class="tbl">
    <thead><tr><th>Partner</th><th>B-Ring-Typ</th><th>O-Atome am Ring</th><th>Rolle</th></tr></thead>
    <tbody>
      <tr><td>(−)-Epicatechin · EC</td><td>Brenzcatechin (3',4'-diOH)</td><td>2</td>
          <td>wird zuerst zum Chinon → Elektrophil</td></tr>
      <tr><td>(−)-Epigallocatechin · EGC</td><td>Pyrogallol (3',4',5'-triOH)</td><td>3</td>
          <td>bleibt reduziert → Nucleophil</td></tr>
    </tbody>
  </table>

  {fig("substrate", "Die beiden Substrate. Der Mechanismus spielt sich ausschließlich am "
       "B-Ring ab; A- und C-Ring bleiben unangetastet. In allen folgenden Bildern ist das "
       "ganze Flavan-3-ol deshalb zu <b>EC</b> bzw. <b>EGC</b> abgekürzt und nur der B-Ring "
       "voll ausgezeichnet.")}
</header>

<section class="step">
  <p class="eyebrow">Schritt 0</p>
  <h2>PPO oxidiert den B-Ring zum <i>o</i>-Chinon</h2>
  <p>Enzym: Polyphenoloxidase mit Typ-3-Kupferzentrum — zwei Cu, verbrückt durch ein
  μ-η²:η²-Peroxo aus O₂. Catecholase-Aktivität:
  <code>o-Diphenol + ½ O₂ → o-Chinon + H₂O</code>. Das Substrat wird am Kupfer deprotoniert;
  gezeichnet wird deshalb vom Catecholat aus.</p>

  {fig("step0", "Die Aromatizität des B-Rings wird gegen zwei Carbonylgruppen eingetauscht. "
       "Was entsteht, ist kein normales Dien und kein normales Keton, sondern ein "
       "gekreuzt-konjugiertes Dien-dion — und genau das ist der Punkt.")}

  {pf(("1", "Das freie Elektronenpaar des 4'-Sauerstoffs klappt in die C4'–O-σ-Bindung "
            "hinein → π(C4'=O) entsteht."),
      ("2", "Dasselbe am 3'-Sauerstoff: sein Elektronenpaar geht in die C3'–O-Bindung "
            "→ π(C3'=O)."),
      ("3", "Damit die Valenzen aufgehen, muss der Ring bezahlen: die π-Bindung C3'=C4' "
            "gibt ihre zwei Elektronen ab. Sie fließen auf das Cu(II)₂-Peroxo "
            "→ Cu(I)₂ + H₂O."))}

  <p><b>Was bricht:</b> die Aromatizität des B-Rings. <b>Was entsteht:</b> ein Elektrophil.</p>

  {merk("Der Ring gibt seine Aromatizität ab wie ein Pfand — und wird dafür zum Elektrophil. "
        "Ein Phenol ist elektronenreich und will geben; ein Chinon ist elektronenarm und will "
        "nehmen. Dieselbe Struktur, zwei Elektronen Unterschied, komplett gegensätzliche Rolle. "
        "Das ist das ganze Prinzip der oxidativen Kupplung — du brauchst es wieder bei "
        "Ellagsäure, bei Melanin/Tyrosinase und bei der Kakao-Bräunung.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 1</p>
  <h2>Redox-Austausch: warum nie beide gleichzeitig oxidiert sind</h2>
  <p>Ein <i>o</i>-Chinon ist selbst ein Oxidationsmittel. Es steht mit dem reduzierten
  Partner im Gleichgewicht:</p>

  {fig("step1", "EC-Chinon + EGC ⇌ EC + EGC-Chinon. Im Gemisch liegt immer ein Paar aus "
       "einem oxidierten (elektrophilen) und einem reduzierten (nucleophilen) Partner vor.")}

  <p>Das ist die Antwort auf „warum reagiert überhaupt etwas“: <b>zwei Chinone reagieren
  nicht miteinander, zwei Catechine auch nicht.</b> Es braucht das Paar.</p>

  {merk("Das Chinon ist der Dieb, der herumläuft und Elektronen klaut. Sobald es zwei "
        "geklaut hat, ist es selbst wieder ein Phenol — und der Beklaute ist jetzt der Dieb.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 2</p>
  <h2>Erste C–C-Kupplung, Michael-analog</h2>
  <p><b>Elektrophil</b> = EC-Chinon (Brenzcatechin-Typ). <b>Nucleophil</b> = EGC (Pyrogallol-Typ,
  reduziert). Die Rollenverteilung folgt aus der Elektronendichte, und zwar positionsgenau.</p>

  <h3>Warum greift <em class="pos">EGC</em> an?</h3>
  <p>Am Pyrogallol-Ring sind nur <em class="pos">C-2'</em> und <em class="pos">C-6'</em>
  unsubstituiert. Nimm C-2': er ist <b>ortho</b> zur 3'-OH (+M) <b>und para</b> zur 5'-OH (+M)
  — zwei Hydroxylgruppen beliefern dieselbe Position. Am Brenzcatechin-Ring ist jede freie
  Position nur von <i>einer</i> OH aktiviert; mit zwei Sauerstoffen geht nicht mehr.
  Der Pyrogallol-Ring ist also der bessere Donor.</p>

  <h3>Und welcher Kohlenstoff am Chinon ist elektrophil?</h3>
  <p>Zeichne das <i>o</i>-Chinon mit C1'=C2' und C5'=C6'. Dann hast du zwei Enon-Systeme:</p>
  <p><code>O=C3'–C2'=C1'</code> → β-C ist C-1' — <b>blockiert</b>, dort sitzt der Flavan-C-Ring.<br>
  <code>O=C4'–C5'=C6'</code> → β-C ist C-6' — <b>frei</b>. Damit ist C-6' die Michael-Position.</p>

  {fig("step2", "Michael-Addition, nur dass der Donor ein ganzer Aromat ist. Der vierte, "
       "nicht nummerierte Pfeil rechts oben ist der Pflichtpartner von Pfeil 3: ohne ihn "
       "hätte C-4' fünf Bindungen. Ergebnis ist ein Zwitterion — links ein Arenium-Kation, "
       "rechts ein Enolat.")}

  {pf(("1", "Das freie Elektronenpaar des 3'-O am EGC klappt in den Ring (+M) und schiebt "
            "Elektronendichte nach C-2'."),
      ("2", "Die π-Bindung C1'=C2' des EGC greift mit C-2' den C-6' des EC-Chinons an. "
            "Neue σ-C–C-Bindung: C2'(EGC)–C6'(EC)."),
      ("3", "Am Chinon bricht π(C5'=C6') auf und klappt auf C-4' um; gleichzeitig geht "
            "π(C4'=O) auf den Sauerstoff → Enolat am 4'-O⁻."))}

  {merk("Michael-Addition — nur dass der „Enolester“ hier ein ganzer Aromat ist. "
        "1,4-Addition, wie du sie von jedem α,β-ungesättigten Keton kennst.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 3</p>
  <h2>Rearomatisierung: der Motor der ganzen Reaktion</h2>
  <p>Jetzt sitzt <b>auf beiden Seiten der neuen Bindung</b> ein sp³-Kohlenstoff mit einem
  Wasserstoff: C-2' am EGC-Fragment und C-6' am EC-Fragment. Beide müssen weg, damit beide
  Ringe wieder aromatisch werden.</p>

  {fig("step3", "Beide H stehen links und rechts der Bindungsstelle. Die nicht nummerierten "
       "Pfeile sind die Pflichtpartner: die frei werdenden C–H-Elektronenpaare klappen in den "
       "jeweiligen Ring, und das Enolat wird protoniert.")}

  {pf(("4", "Eine Base nimmt das Proton an C-2' des EGC-Fragments ab."),
      ("5", "Das frei werdende Elektronenpaar klappt in den Ring → der EGC-Ring ist "
            "wieder aromatisch."),
      ("6", "Dasselbe am EC-Fragment: Base nimmt das H an C-6', die Elektronen gehen in den "
            "Ring, das Enolat-O wird protoniert → zurück zum Brenzcatechin."))}

  <p>Warum läuft das? Weil <b>Aromatizität zurückgewonnen wird</b> — das ist die
  thermodynamische Triebkraft. Glomb sagt es in der VL fast wörtlich: „… kann sich jetzt das
  aromatische System durch Zuhilfenahme dieser Elektronenpaare, die diese Protonen links und
  rechts der Bindungsstelle beinhalten, dann zurückführen, sodass Sie eine stabile kovalente
  Vernetzung dieser phenolischen Strukturen haben.“</p>

  <div class="note">
    <p><span class="mk">Zum Mitschreiben</span>
    „Links und rechts der Bindungsstelle“ ist wörtlich zu nehmen: es sind
    <b>zwei</b> Protonen, eines pro Ring. Wer nur eines abzieht, bekommt die Bilanz nicht auf —
    das Chinon nimmt genau die zwei H auf, die es beim Rearomatisieren als Catechin zurückbraucht.</p>
  </div>

  {fig("biaryl", "Stand jetzt: Biaryl, beide Ringe reduziert, beide aromatisch, farblos. "
       "Bis hierhin ist es exakt dieselbe Reaktion wie Gallussäure → Ellagsäure. "
       "Noch keine Farbe.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 4</p>
  <h2>Dritte Oxidation — und diesmal trifft es den Pyrogallol-Ring</h2>
  <p>PPO (oder das nächste <i>o</i>-Chinon als Oxidationsmittel) oxidiert erneut. Ziel ist
  jetzt der Pyrogallol-Ring: er trägt nach der Kupplung einen zusätzlichen
  elektronenschiebenden Aryl-Substituenten, ist also noch elektronenreicher und noch leichter
  oxidierbar. <b>Das niedrigste Oxidationspotential gewinnt.</b></p>

  {fig("step4", "Aus dem Pyrogallol-Ring wird ein Hydroxy-o-chinon: C3'=O, C4'=O, "
       "5'-OH bleibt stehen. Damit ist das Elektrophil für die zweite Kupplung fertig.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 5</p>
  <h2>Zweite, intramolekulare Kupplung → der Tricyclus</h2>
  <p>Jetzt sitzen Nucleophil und Elektrophil im selben Molekül, im Abstand einer Bindung.
  Das ist keine Konkurrenz mehr, das ist Geometrie.</p>

  {fig("step5", "Diesmal keine Michael-Addition: der Angriff geht direkt auf den "
       "Carbonyl-Kohlenstoff, also 1,2-Addition. C-5' des EC-Rings ist ortho zur 4'-OH, "
       "elektronenreich und liegt direkt neben der schon geknüpften Bindung an C-6'.")}

  {pf(("7", "C-5' des EC-Rings greift den Carbonyl-Kohlenstoff C-4' des Pyrogallol-Chinons an."),
      ("8", "Die π-Bindung C4'=O bricht heterolytisch auf, die Elektronen gehen auf den "
            "Sauerstoff → Alkoholat an C-4'."))}

  <p>Anschließend rearomatisiert der EC-Ring wieder durch Abgabe des H an C-5' — dieselbe
  Buchhaltung wie in Schritt 3. Gezeichnet ist unten bereits die rearomatisierte Form.</p>

  {fig("bicycle", "Zwei Ringe, die sich an zwei Stellen die Hand geben. Die zweite C–C-Bindung "
       "spannt zusammen mit der ersten einen Fünfring auf: "
       "C6'(EC)–C5'(EC)–C4'(EGC)–C3'(EGC)–C2'(EGC). Mit den beiden Sechsringen sind das drei "
       "Ringe — der „Tricyclus“ aus dem Skript, formal ein Bicyclo[3.2.1]-Gerüst. "
       "Der Siebenring, auf den alles hinausläuft, liegt darin bereits fertig vor; "
       "C-3' (kupferfarben) liegt nur noch quer darüber.")}

  {merk("Zwei Ringe, die sich an zwei Stellen die Hand geben — dazwischen wird ein "
        "Kohlenstoff eingeklemmt, der gleich rausfliegt.")}

  <p>Dieser eingeklemmte Kohlenstoff ist <em class="pos">C-3'</em> des Pyrogallol-Rings.
  Er trägt jetzt eine C=O-Funktion, links und rechts je eine C–C-Bindung, und sein Nachbar
  C-4' ist ein Alkoholat. <b>Das ist ein α-Ketol</b> — und α-Ketole spalten.</p>
</section>

<section class="step">
  <p class="eyebrow">Schritt 6</p>
  <h2>CO₂ raus, Siebenring rein</h2>

  {fig("step6", "Retro-Aldol am α-Ketol, dann Decarboxylierung. Die kupferfarbene Brücke ist "
       "genau der Kohlenstoff, der das Molekül als CO₂ verlässt.")}

  {pf(("9", "Retro-Aldol / α-Ketol-Spaltung: das freie Elektronenpaar des Alkoholats an C-4' "
            "klappt herunter, C4'=O bildet sich neu."),
      ("10", "Dabei bricht die σ-Bindung C4'–C3'. Die Elektronen dieser Bindung bleiben "
             "bei C-3'; nach Protonierung und Hydratisierung wird daraus eine Carboxylgruppe, "
             "die nur noch an C-2' hängt. Der Ring des Pyrogallol-Fragments ist aufgerissen."),
      ("11", "Decarboxylierung: die COOH-Gruppe steht β zum entstandenen Carbonyl — klassische "
             "β-Ketosäure-Spaltung. Die C–C-Bindung zur COOH bricht, die Elektronen laufen "
             "über das Carbonyl ins Enolat, CO₂ fliegt raus."),
      ("12", "Tautomerisierung / Protonenverschiebung: das Tropolon-System stellt sich ein — "
             "eine C=O und eine benachbarte OH im Siebenring."))}

  <h3>Jetzt zählen</h3>
  <p>Vom Pyrogallol-Ring sind noch fünf Kohlenstoffe da: C-1', C-2', C-4', C-5', C-6'.
  Sie hängen über die zwei neuen Bindungen an C-5' und C-6' des EC-Rings.
  <b>5 + 2 = 7.</b> Der Siebenring ist da.</p>

  {fig("product", "Benzotropolon: ein Benzolring, anelliert an einen Siebenring, der eine "
       "C=O und eine benachbarte OH trägt. Das ist das Kerngerüst der Theaflavine.")}
</section>

<section class="step">
  <p class="eyebrow">Schritt 7</p>
  <h2>Und deshalb ist es kupferrot</h2>

  {fig("chromophore", "Ein Siebenring, der aromatisch ist, weil er formal ein Kation ist: "
       "die OH schiebt ihr Elektronenpaar in den Ring, die C=O zieht — übrig bleibt ein "
       "Tropylium-artiges 6π-System mit Oxyanion.")}

  <div class="answer">
    <h2>Die Antwort in drei Sätzen</h2>
    <ol>
      <li><b>Ein Tropolon ist aromatisch — aber nicht benzoid.</b> Die OH-Gruppe schiebt ihr
      Elektronenpaar in den Ring, die C=O zieht; das Ringsystem stabilisiert sich als
      Tropylium-artiges 6π-System mit Oxyanion.</li>
      <li><b>Das Molekül ist ein eingebautes Donor-Akzeptor-Paar.</b> Die phenolischen OH am
      Benzolteil sind der Donor, das Tropolon-Carbonyl ist der Akzeptor — und sie sind über
      das anellierte, durchkonjugierte 11-C-System direkt gekoppelt. Ergebnis: starker
      intramolekularer Charge-Transfer.</li>
      <li><b>Deshalb fällt der HOMO–LUMO-Abstand ins Sichtbare.</b> Absorbiert wird im
      Blaugrünen — was durchkommt, ist kupferrot.</li>
    </ol>
  </div>

  <div class="note">
    <p><span class="mk">Einordnung</span>
    Dieselbe Chemie mit denselben Pfeilen läuft an drei Stellen, die im StEx gern
    zusammen abgefragt werden: <b>Gallussäure → Ellagsäure</b> (bleibt beim Biaryl stehen,
    farblos), <b>Tyrosinase → Melanin</b> (o-Chinon aus DOPA, dann Cyclisierung) und die
    <b>Bräunung von Kakao, Tee und Apfel</b> (PPO auf Epicatechin und Procyanidinen).
    Nur wo ein Pyrogallol-Ring mitspielt, kommt der Siebenring — und damit die Farbe — heraus.</p>
  </div>
</section>

<footer>
  <p>Strukturformeln aus gerechneten Koordinaten erzeugt (<code>generate.py</code>),
  Seite gebaut mit <code>build.py</code>. Bindungslänge = Sechseck-Umkreisradius,
  alle Pfeile mit vollständiger Elektronenbuchhaltung.</p>
</footer>

</div>
"""

out = HERE / "mechanismus.html"
out.write_text(
    f'<title>Oxidative Kupplung: vom Catechin zum Benzotropolon</title>\n'
    f'<style>{CSS}</style>\n{BODY}', encoding="utf-8")
print("geschrieben:", out, out.stat().st_size, "bytes")
