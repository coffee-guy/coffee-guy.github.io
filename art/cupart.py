"""Write the menu-card artwork (a small and a medium cup, two band colours) into docs/images."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chars import cup  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "docs" / "images"
SAUCER_BOTTOM = 598 + 40.5  # cup() draws around (205, 598)


def cups(band):
    parts = ['<ellipse cx="150" cy="190" rx="136" ry="12" fill="#5b3420" opacity=".2"/>']
    for x, scale in ((78, 1.14), (212, 1.4)):
        art = cup(205, 598, 56, "right", True, "#fff", lw=0.75 / scale, band_color=band)
        parts.append(f'<g transform="translate({x} 186) scale({scale}) translate(-205 {-SAUCER_BOTTOM})">{art}</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 210" width="300" height="210">{"".join(parts)}</svg>'


for name, band in (("saffron", "#f3b23c"), ("teal", "#2f8f8b")):
    path = OUT / f"cups-{name}.svg"
    path.write_text(cups(band), encoding="utf-8")
    print("wrote", path)
