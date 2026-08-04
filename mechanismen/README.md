# Mechanismen

Strukturformeln und Mechanismus-Seiten für das LMC-Staatsexamen.

## Oxidative Kupplung → Benzotropolon (Theaflavin)

EC + EGC unter Polyphenoloxidase: von der Chinonbildung über die
Michael-analoge C–C-Kupplung und den Bicyclo[3.2.1]-Tricyclus bis zum
kupferroten Benzotropolon-Chromophor.

| Datei | Zweck |
|---|---|
| `generate.py` | erzeugt alle SVG-Strukturformeln aus gerechneten Koordinaten → `figures.py` |
| `figures.py` | generiert, nicht von Hand ändern |
| `build.py` | setzt Figuren + Text zu `mechanismus.html` zusammen |
| `mechanismus.html` | fertige Seite, in sich geschlossen (kein CDN, kein Script) |
| `proof.py` | Entwicklungshilfe: rendert die Figuren als PNG zur Sichtkontrolle |

```
python3 generate.py && python3 build.py
```

### Konventionen der Zeichnungen

* Bindungslänge = Umkreisradius des Sechsecks (`BOND = 34`); jede Koordinate
  wird gerechnet, nichts wird geschätzt.
* Formeln mit Hoch-/Tiefstellung werden aus einzelnen `<text>`-Elementen
  gesetzt und über Helvetica-Vorschubbreiten positioniert — keine `tspan`-`dy`,
  die je nach Renderer unterschiedlich kumulieren.
* Kupferfarbe ist ausschließlich Elektronenfluss (und am Ende die Produktfarbe),
  Petrol ausschließlich Sauerstoff.
* Nummerierte Pfeile folgen der Nummerierung im Fließtext. Nicht nummerierte
  Pfeile sind Pflichtpartner, ohne die die Valenzbilanz nicht aufginge.

### Abweichung von der Kurzfassung

In Schritt 3 gehen **zwei** Protonen ab, eines pro Ring — das ist Glombs
„Protonen links und rechts der Bindungsstelle“ wörtlich genommen und die
einzige Lesart, mit der die H-Bilanz aufgeht.
