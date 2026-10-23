"""Render an SVG with headless Edge: one full view plus optional zoomed crops side by side.

python art/preview.py logo.svg out.png [--full 640] [--crop x,y,w,h[,px]] ...
"""
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("svg")
p.add_argument("png")
p.add_argument("--full", type=int, default=640, help="size of the full view (0 = none)")
p.add_argument("--crop", action="append", default=[], help="x,y,w,h[,px] in logo units (800 box), px = output size")
p.add_argument("--bg", default="#fff4e3")
a = p.parse_args()

svg = Path(a.svg).resolve()
panels = []
if a.full:
    panels.append(f'<div style="width:{a.full}px;height:{a.full}px;overflow:hidden"><img src="{svg.as_uri()}" style="width:{a.full}px;height:{a.full}px;display:block"></div>')
total_w = a.full if a.full else 0
height = a.full if a.full else 0
for c in a.crop:
    parts = [float(v) for v in c.split(",")]
    x, y, w, h = parts[:4]
    px = int(parts[4]) if len(parts) > 4 else 560
    k = px / w  # px per logo unit
    ph = int(h * k)
    panels.append(
        f'<div style="width:{px}px;height:{ph}px;overflow:hidden;position:relative">'
        f'<img src="{svg.as_uri()}" style="position:absolute;left:{-x * k}px;top:{-y * k}px;width:{800 * k}px;height:{800 * k}px;max-width:none"></div>'
    )
    total_w += px
    height = max(height, ph)

edge = Path(os.environ.get("ProgramFiles(x86)", "")) / "Microsoft/Edge/Application/msedge.exe"
with tempfile.TemporaryDirectory() as tmp:
    page = Path(tmp) / "p.html"
    page.write_text(
        f'<!doctype html><body style="margin:0;background:{a.bg};display:flex;gap:0;align-items:flex-start">{"".join(panels)}</body>',
        encoding="utf-8",
    )
    subprocess.run(
        [str(edge), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={Path(tmp) / 'profile'}",
         f"--window-size={max(total_w, 500)},{max(height, 300)}", "--virtual-time-budget=3000",
         f"--screenshot={Path(a.png).resolve()}", page.as_uri()],
        check=True, capture_output=True, timeout=120,
    )
print("wrote", a.png)
