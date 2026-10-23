"""Write docs/images/coffee-cup.svg: the logo's cup and saucer, enlarged, for the menu cards."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from chars import cup  # noqa: E402

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "docs" / "images" / "coffee-cup.svg"
art = cup(205, 598, 56, "right", True, "#fff", lw=0.55)
svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 224" width="240" height="224">'
    '<ellipse cx="120" cy="206" rx="104" ry="13" fill="#5b3420" opacity=".22"/>'
    '<g transform="translate(120 110) scale(2.15) translate(-205 -594)">' + art + "</g></svg>"
)
out.write_text(svg, encoding="utf-8")
print("wrote", out, len(svg), "bytes")
