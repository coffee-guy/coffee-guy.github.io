"""Generate the website QR code in ./qr: a plain code and a "SCAN ME" poster, each as PNG and SVG."""

import argparse
import os
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import segno

OUT_DIR = Path(__file__).resolve().parent / "qr"
LOGO = Path(__file__).resolve().parent / "docs" / "images" / "logo.svg"

ESPRESSO, SAFFRON, CREAM, PAPER = "#2b1810", "#f3b23c", "#fff4e3", "#f6ecd9"

# Bebas Neue (SIL OFL) outlined as vector paths; capitals are 100 units tall.
GLYPHS = {
    "A": (57.3, "M18 0H39.3L55.6 100H39.9L37 80.1V80.4H19.1L16.3 100H1.7ZM35.1 66.9 28.1 17.4H27.9L21 66.9Z"),
    "B": (57.7, "M5.9 0H29.6Q41.7 0 47.3 5.6Q52.9 11.3 52.9 23V27Q52.9 34.7 50.4 39.6Q47.9 44.4 42.7 46.6V46.9Q54.4 50.9 54.4 67.7V76.3Q54.4 87.9 48.4 93.9Q42.3 100 30.6 100H5.9ZM27.7 40.7Q32.4 40.7 34.8 38.3Q37.1 35.9 37.1 30.1V24.6Q37.1 19.1 35.2 16.7Q33.3 14.3 29.1 14.3H21.6V40.7ZM30.6 85.7Q34.7 85.7 36.7 83.5Q38.7 81.3 38.7 75.9V67.1Q38.7 60.3 36.4 57.6Q34 55 28.6 55H21.6V85.7Z"),
    "C": (54.7, "M4.9 76.9V23.1Q4.9 11.4 10.8 5Q16.7 -1.4 28 -1.4Q39.3 -1.4 45.2 5Q51.1 11.4 51.1 23.1V33.7H36.3V22.1Q36.3 12.9 28.4 12.9Q20.6 12.9 20.6 22.1V78Q20.6 87.1 28.4 87.1Q36.3 87.1 36.3 78V62.7H51.1V76.9Q51.1 88.6 45.2 95Q39.3 101.4 28 101.4Q16.7 101.4 10.8 95Q4.9 88.6 4.9 76.9Z"),
    "D": (58.0, "M5.9 0H29.9Q41.6 0 47.4 6.3Q53.3 12.6 53.3 24.7V75.3Q53.3 87.4 47.4 93.7Q41.6 100 29.9 100H5.9ZM29.6 85.7Q33.4 85.7 35.5 83.4Q37.6 81.1 37.6 76V24Q37.6 18.9 35.5 16.6Q33.4 14.3 29.6 14.3H21.6V85.7Z"),
    "E": (51.9, "M5.9 0H48.7V14.3H21.6V40.7H43.1V55H21.6V85.7H48.7V100H5.9Z"),
    "F": (49.1, "M5.9 0H47.4V14.3H21.6V42.1H41.9V56.4H21.6V100H5.9Z"),
    "G": (55.9, "M4.7 76.3V23.7Q4.7 11.6 10.7 5.1Q16.7 -1.4 28.1 -1.4Q39.6 -1.4 45.6 5.1Q51.6 11.6 51.6 23.7V32.3H36.7V22.7Q36.7 12.9 28.6 12.9Q20.4 12.9 20.4 22.7V77.4Q20.4 87.1 28.6 87.1Q36.7 87.1 36.7 77.4V57.9H28.9V43.6H51.6V76.3Q51.6 88.4 45.6 94.9Q39.6 101.4 28.1 101.4Q16.7 101.4 10.7 94.9Q4.7 88.4 4.7 76.3Z"),
    "H": (60.0, "M5.9 0H21.6V40.7H38.4V0H54.1V100H38.4V55H21.6V100H5.9Z"),
    "I": (27.4, "M5.9 0H21.6V100H5.9Z"),
    "J": (37.9, "M2.3 100V85.7Q4.6 86.3 7.4 86.3Q12.1 86.3 14.4 83.9Q16.7 81.6 16.7 76.7V0H32.4V76.3Q32.4 88.6 26.8 94.6Q21.1 100.6 9.6 100.6Q5.3 100.6 2.3 100Z"),
    "K": (59.1, "M5.9 0H21.6V42.1L41.6 0H57.3L38.6 36.7L57.6 100H41.1L27.9 55.4L21.6 68.1V100H5.9Z"),
    "L": (49.1, "M5.9 0H21.6V85.7H47.4V100H5.9Z"),
    "M": (76.9, "M5.9 0H28.3L38.3 71.6H38.6L48.6 0H71V100H56.1V24.3H55.9L44.4 100H31.3L19.9 24.3H19.6V100H5.9Z"),
    "N": (61.0, "M5.9 0H25.6L40.9 59.9H41.1V0H55.1V100H39L20.1 27H19.9V100H5.9Z"),
    "O": (57.1, "M4.7 76.3V23.7Q4.7 11.7 10.9 5.1Q17 -1.4 28.6 -1.4Q40.1 -1.4 46.3 5.1Q52.4 11.7 52.4 23.7V76.3Q52.4 88.3 46.3 94.9Q40.1 101.4 28.6 101.4Q17 101.4 10.9 94.9Q4.7 88.3 4.7 76.3ZM36.7 77.3V22.7Q36.7 12.9 28.6 12.9Q20.4 12.9 20.4 22.7V77.3Q20.4 87.1 28.6 87.1Q36.7 87.1 36.7 77.3Z"),
    "P": (55.1, "M5.9 0H29Q40.7 0 46.6 6.3Q52.4 12.6 52.4 24.7V34.6Q52.4 46.7 46.6 53Q40.7 59.3 29 59.3H21.6V100H5.9ZM29 45Q32.9 45 34.8 42.9Q36.7 40.7 36.7 35.6V23.7Q36.7 18.6 34.8 16.4Q32.9 14.3 29 14.3H21.6V45Z"),
    "Q": (57.1, "M39 99.7Q34.6 101.4 28.6 101.4Q17 101.4 10.9 94.9Q4.7 88.3 4.7 76.3V23.7Q4.7 11.7 10.9 5.1Q17 -1.4 28.6 -1.4Q40.1 -1.4 46.3 5.1Q52.4 11.7 52.4 23.7V76.3Q52.4 86.3 48 92.7Q48.9 94.1 50.1 94.6Q51.4 95 53.9 95H56.3V109.3H52.1Q41.4 109.3 39 99.7ZM36.7 77.3V22.7Q36.7 12.9 28.6 12.9Q20.4 12.9 20.4 22.7V77.3Q20.4 87.1 28.6 87.1Q36.7 87.1 36.7 77.3Z"),
    "R": (57.6, "M5.9 0H29.1Q41.3 0 46.9 5.6Q52.4 11.3 52.4 23V29.1Q52.4 44.7 42.1 48.9V49.1Q47.9 50.9 50.2 56.1Q52.6 61.4 52.6 70.3V87.9Q52.6 92.1 52.9 94.8Q53.1 97.4 54.3 100H38.3Q37.4 97.6 37.1 95.4Q36.9 93.3 36.9 87.7V69.4Q36.9 62.6 34.6 59.9Q32.4 57.1 27 57.1H21.6V100H5.9ZM27.3 42.9Q32 42.9 34.4 40.4Q36.7 38 36.7 32.3V24.6Q36.7 19.1 34.8 16.7Q32.9 14.3 28.7 14.3H21.6V42.9Z"),
    "S": (53.1, "M3.1 76.3V70.6H18V77.4Q18 87.1 26.1 87.1Q30.1 87.1 32.2 84.8Q34.3 82.4 34.3 77.1Q34.3 70.9 31.4 66.1Q28.6 61.3 20.9 54.6Q11.1 46 7.3 39.1Q3.4 32.1 3.4 23.4Q3.4 11.6 9.4 5.1Q15.4 -1.4 26.9 -1.4Q38.1 -1.4 43.9 5.1Q49.7 11.6 49.7 23.7V27.9H34.9V22.7Q34.9 17.6 32.9 15.2Q30.9 12.9 27 12.9Q19.1 12.9 19.1 22.4Q19.1 27.9 22.1 32.6Q25 37.3 32.7 44Q42.6 52.6 46.3 59.6Q50 66.6 50 76Q50 88.3 43.9 94.9Q37.9 101.4 26.3 101.4Q14.9 101.4 9 94.9Q3.1 88.4 3.1 76.3Z"),
    "T": (52.0, "M18.1 14.3H1.7V0H50.3V14.3H33.9V100H18.1Z"),
    "U": (57.4, "M5.3 76.3V0H21V77.4Q21 82.6 23.1 84.9Q25.1 87.1 29 87.1Q32.9 87.1 34.9 84.9Q37 82.6 37 77.4V0H52.1V76.3Q52.1 88.4 46.1 94.9Q40.1 101.4 28.7 101.4Q17.3 101.4 11.3 94.9Q5.3 88.4 5.3 76.3Z"),
    "V": (54.6, "M1.7 0H17.6L27.9 77.6H28.1L38.4 0H52.9L37.7 100H16.9Z"),
    "W": (79.6, "M2.1 0H17.3L24.3 76.9H24.6L32 0H49.1L56.6 76.9H56.9L63.9 0H77.4L67.3 100H47.7L40.6 32.6H40.3L33.1 100H12.3Z"),
    "X": (58.0, "M19.7 48.9 2.4 0H19L29.6 32.3H29.9L40.7 0H55.6L38.3 48.9L56.4 100H39.9L28.4 65.1H28.1L16.4 100H1.6Z"),
    "Y": (56.3, "M20.3 57.4 1.3 0H18L28.7 36.7H29L39.7 0H55L36 57.4V100H20.3Z"),
    "Z": (51.7, "M2.7 86 31.9 14.3H4.1V0H48.7V14L19.6 85.7H48.7V100H2.7Z"),
    "0": (57.1, "M4.7 76.3V23.7Q4.7 11.7 10.9 5.1Q17 -1.4 28.6 -1.4Q40.1 -1.4 46.3 5.1Q52.4 11.7 52.4 23.7V76.3Q52.4 88.3 46.3 94.9Q40.1 101.4 28.6 101.4Q17 101.4 10.9 94.9Q4.7 88.3 4.7 76.3ZM36.7 77.3V22.7Q36.7 12.9 28.6 12.9Q20.4 12.9 20.4 22.7V77.3Q20.4 87.1 28.6 87.1Q36.7 87.1 36.7 77.3Z"),
    "1": (57.1, "M27.9 23.7H11.4V12.6Q18.1 12.6 22.2 11.4Q26.3 10.3 28.7 7.6Q31.1 5 33 0H43.6V100H27.9Z"),
    "2": (57.1, "M5.6 89.1Q5.6 78.4 9 70.8Q12.4 63.1 21.3 53.9Q30 44.6 33.4 38Q36.7 31.4 36.7 24.3Q36.7 17.9 34.6 15.4Q32.6 12.9 28.6 12.9Q20.4 12.9 20.4 22.7V33.4H5.6V23.7Q5.6 11.6 11.6 5.1Q17.6 -1.4 29 -1.4Q40.4 -1.4 46.4 5.1Q52.4 11.6 52.4 23.7Q52.4 32.9 48.1 41.6Q43.7 50.3 33 61.6Q26 69 23.6 73.6Q21.1 78.3 21.1 83.6V85.7H51V100H5.6Z"),
    "3": (57.1, "M4.7 76.6V68.4H19.6V77.3Q19.6 87.1 27.7 87.1Q31.7 87.1 33.8 84.6Q35.9 82.1 35.9 75.9V67.7Q35.9 60.9 33.4 57.9Q31 55 25.6 55H20.3V40.7H26Q30.7 40.7 33.1 38.3Q35.4 35.9 35.4 30.1V22.9Q35.4 17.7 33.3 15.3Q31.1 12.9 27.6 12.9Q20 12.9 20 22.1V28.7H5.1V23.4Q5.1 11.4 11.1 5Q17 -1.4 28.1 -1.4Q39.4 -1.4 45.3 4.9Q51.1 11.3 51.1 23.3V26.9Q51.1 35 48.4 39.9Q45.7 44.9 40 47V47.3Q46.1 49.6 48.9 54.7Q51.6 59.9 51.6 67.9V76.7Q51.6 88.7 45.6 95.1Q39.7 101.4 28.1 101.4Q16.6 101.4 10.6 95Q4.7 88.6 4.7 76.6Z"),
    "4": (57.1, "M32.1 81.9H2.1V67.6L30.7 0H47.9V67.6H55.3V81.9H47.9V100H32.1ZM32.1 67.6V28.6H31.9L16.4 67.6Z"),
    "5": (57.1, "M5.4 76.3V68.4H20.3V77.4Q20.3 87.1 28.4 87.1Q36.6 87.1 36.6 77.4V55Q36.6 45.1 28.4 45.1Q20.3 45.1 20.3 55V55.9H5.4L8.3 0H49.7V14.3H22.3L21 38.1H21.3Q25.7 30.9 34.9 30.9Q43.4 30.9 47.9 36.7Q52.3 42.6 52.3 53.7V76.3Q52.3 88.4 46.3 94.9Q40.3 101.4 28.9 101.4Q17.4 101.4 11.4 94.9Q5.4 88.4 5.4 76.3Z"),
    "6": (57.1, "M5.1 76.3V24.6Q5.1 -1.4 29.1 -1.4Q40.6 -1.4 46.6 5.1Q52.6 11.6 52.6 23.7V25.6H37.7V22.7Q37.7 12.9 29.6 12.9Q25.1 12.9 23 15.6Q20.9 18.3 20.9 25.1V44.3H21.1Q25.3 35.6 35.4 35.6Q44 35.6 48.4 41.4Q52.9 47.3 52.9 58.4V76.3Q52.9 88.3 46.7 94.9Q40.6 101.4 29 101.4Q17.4 101.4 11.3 94.9Q5.1 88.3 5.1 76.3ZM37.1 77.4V59.7Q37.1 49.9 29 49.9Q20.9 49.9 20.9 59.7V77.4Q20.9 87.1 29 87.1Q37.1 87.1 37.1 77.4Z"),
    "7": (57.1, "M36.6 14.3H4.9V0H52V13.7L27.4 100H11.4Z"),
    "8": (57.1, "M4 76.7V67.9Q4 60.4 6.4 55.4Q8.9 50.3 14.3 47.4V47.1Q9.3 44.4 6.9 39.6Q4.6 34.9 4.6 27.4V23.3Q4.6 11.3 10.8 4.9Q17 -1.4 28.6 -1.4Q40.1 -1.4 46.4 4.9Q52.6 11.3 52.6 23.3V27.4Q52.6 41.7 42.9 47.1V47.4Q48.3 50.3 50.7 55.4Q53.1 60.4 53.1 67.9V76.7Q53.1 88.7 46.8 95.1Q40.4 101.4 28.6 101.4Q16.7 101.4 10.4 95.1Q4 88.7 4 76.7ZM36.9 30.7V22.9Q36.9 12.9 28.6 12.9Q20.3 12.9 20.3 22.9V30.7Q20.3 40.7 28.6 40.7Q36.9 40.7 36.9 30.7ZM37.4 75.9V66.3Q37.4 55 28.6 55Q19.7 55 19.7 66.3V75.9Q19.7 87.1 28.6 87.1Q37.4 87.1 37.4 75.9Z"),
    "9": (57.1, "M4.6 76.3V74.4H19.4V77.3Q19.4 87.1 27.6 87.1Q32 87.1 34.1 84.4Q36.3 81.7 36.3 74.9V55.7H36Q31.9 64.4 21.7 64.4Q13.1 64.4 8.7 58.6Q4.3 52.7 4.3 41.6V23.7Q4.3 11.7 10.4 5.1Q16.6 -1.4 28.1 -1.4Q39.7 -1.4 45.9 5.1Q52 11.7 52 23.7V75.4Q52 101.4 28 101.4Q16.6 101.4 10.6 94.9Q4.6 88.4 4.6 76.3ZM36.3 40.3V22.6Q36.3 12.9 28.1 12.9Q20 12.9 20 22.6V40.3Q20 50.1 28.1 50.1Q36.3 50.1 36.3 40.3Z"),
    ".": (26.9, "M5.9 84.9H21V100H5.9Z"),
    "-": (38.6, "M3.6 42.9H35V57.1H3.6Z"),
    "/": (55.6, "M40.7 0H54.3L14.9 100H1.3Z"),
    ":": (26.9, "M5.9 30.4H21V45.6H5.9ZM5.9 84.9H21V100H5.9Z"),
}
SPACE = 22.9


def dark_runs(qr):
    """Dark modules as horizontal runs in one SVG path, in module units."""
    parts = []
    for y, row in enumerate(qr.matrix):
        x = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            start = x
            while x < len(row) and row[x]:
                x += 1
            parts.append(f"M{start} {y}h{x - start}v1h{start - x}z")
    return "".join(parts)


def text_group(text, cap, fill, x, y, anchor="start", track=4):
    """Vector lettering with y at the top of the capitals; returns (svg, width in px)."""
    text = text.upper()
    advances = [GLYPHS.get(ch, (SPACE, ""))[0] for ch in text]
    width = (sum(advances) + track * (len(text) - 1)) * cap / 100
    x -= {"start": 0, "middle": width / 2, "end": width}[anchor]
    parts, cx = [], 0.0
    for ch, adv in zip(text, advances):
        d = GLYPHS.get(ch, (SPACE, ""))[1]
        if d:
            parts.append(f'<path transform="translate({cx:.1f})" d="{d}"/>')
        cx += adv + track
    return f'<g transform="translate({x:.1f} {y:.1f}) scale({cap / 100:.4f})" fill="{fill}">{"".join(parts)}</g>', width


def logo_group(x, y, size):
    markup = LOGO.read_text(encoding="utf-8")
    inner = markup[markup.index(">", markup.index("<svg")) + 1 : markup.rindex("</svg>")]
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 400 400">{inner}</svg>'


def poster_svg(qr, url):
    n = len(qr.matrix)
    m = 440 // (n + 8)  # whole-pixel modules keep the edges crisp
    panel = (n + 8) * m
    w, border, pad = 600, 5, 14
    card = panel + 2 * (pad + border)
    card_x, card_y = (w - card) / 2, 252
    qx, qy = card_x + border + pad, card_y + border + pad
    pill_w, pill_h = 340, 78
    pill_x, pill_y = (w - pill_w) / 2, qy + panel + 14
    cy = pill_y + pill_h / 2
    parsed = urlparse(url)
    shown = (parsed.netloc + parsed.path).rstrip("/")
    url_y = pill_y + pill_h + 30
    h = round(url_y + 18 + 40)

    coffee, _ = text_group("COFFEE", 74, ESPRESSO, 236, 44)
    guy, guy_w = text_group("GUY", 50, CREAM, 254, 140)
    sub, _ = text_group("SOUTH INDIAN FILTER COFFEE", 13, ESPRESSO, 236, 218, track=9)
    scan, _ = text_group("SCAN ME", 36, CREAM, w / 2, pill_y + (pill_h - 36) / 2, "middle", 6)
    link, _ = text_group(shown, 18, ESPRESSO, w / 2, url_y, "middle", 8)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <clipPath id="pp-inner"><rect x="26" y="26" width="{w - 52}" height="{h - 52}" rx="12"/></clipPath>
    <filter id="pp-grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5"/>
      <feColorMatrix values="0 0 0 0 .45  0 0 0 0 .32  0 0 0 0 .2  0 0 0 .16 0"/>
    </filter>
  </defs>
  <rect width="{w}" height="{h}" fill="{PAPER}"/>
  <rect width="{w}" height="{h}" filter="url(#pp-grain)"/>
  <g clip-path="url(#pp-inner)" fill="none" stroke="#a9794a" stroke-linecap="round" opacity=".22">
    <circle cx="44" cy="{h - 44}" r="58" stroke-width="7"/>
    <circle cx="44" cy="{h - 44}" r="51" stroke-width="2"/>
  </g>
  <rect x="14" y="14" width="{w - 28}" height="{h - 28}" rx="20" fill="none" stroke="{ESPRESSO}" stroke-width="4"/>
  <rect x="26" y="26" width="{w - 52}" height="{h - 52}" rx="12" fill="none" stroke="{SAFFRON}" stroke-width="1.8"/>

  <circle cx="135" cy="135" r="85" fill="{ESPRESSO}"/>
  {logo_group(44, 44, 170)}
  {coffee}
  <rect x="242" y="134" width="{guy_w + 36}" height="74" rx="10" fill="{SAFFRON}" stroke="{ESPRESSO}" stroke-width="3"/>
  <rect x="236" y="128" width="{guy_w + 36}" height="74" rx="10" fill="{ESPRESSO}" stroke="{ESPRESSO}" stroke-width="3"/>
  {guy}
  {sub}

  <rect x="{card_x + 10}" y="{card_y + 10}" width="{card}" height="{card}" rx="30" fill="{ESPRESSO}"/>
  <rect x="{card_x}" y="{card_y}" width="{card}" height="{card}" rx="30" fill="#fff" stroke="{ESPRESSO}" stroke-width="{border}"/>
  <g transform="translate({qx + 4 * m} {qy + 4 * m}) scale({m})">
    <path d="{dark_runs(qr)}" fill="{ESPRESSO}" shape-rendering="crispEdges"/>
  </g>

  <rect x="{pill_x + 6}" y="{pill_y + 7}" width="{pill_w}" height="{pill_h}" rx="{pill_h / 2}" fill="{SAFFRON}" stroke="{ESPRESSO}" stroke-width="3"/>
  <rect x="{pill_x}" y="{pill_y}" width="{pill_w}" height="{pill_h}" rx="{pill_h / 2}" fill="{ESPRESSO}" stroke="{ESPRESSO}" stroke-width="3"/>
  <g transform="translate({pill_x + 50} {cy})" fill="none" stroke="{SAFFRON}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-15,-6V-15H-6M6,-15H15V-6M15,6V15H6M-6,15H-15V6"/>
    <circle r="2.6" fill="{SAFFRON}" stroke="none"/>
  </g>
  {scan}
  <path transform="translate({pill_x + pill_w - 50} {cy})" d="M0,11V-11M-9,-2L0,-11L9,-2" fill="none" stroke="{SAFFRON}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
  {link}
</svg>"""
    return svg, w, h


def find_edge():
    for var in ("ProgramFiles(x86)", "ProgramFiles"):
        exe = Path(os.environ.get(var, "")) / "Microsoft/Edge/Application/msedge.exe"
        if exe.exists():
            return exe
    return None


def render_png(svg, png, width, height):
    """Rasterise the poster with headless Edge; returns False when Edge is missing."""
    edge = find_edge()
    if not edge:
        return False
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "poster.html"
        page.write_text(
            f"<!doctype html><style>body{{margin:0}}svg{{display:block;width:{width}px;height:{height}px}}</style>{svg}",
            encoding="utf-8",
        )
        subprocess.run(
            [
                str(edge), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--user-data-dir={Path(tmp) / 'profile'}", f"--window-size={width},{height}",
                f"--screenshot={png}", page.as_uri(),
            ],
            check=True, capture_output=True, timeout=120,
        )
    return png.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Final public https:// address of the website")
    parser.add_argument("--name", default="coffeeguy", help="File name prefix")
    parser.add_argument("--out", type=Path, default=OUT_DIR, help="Output folder (default: ./qr)")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme != "https" or not parsed.netloc:
        parser.error("url must be a full https:// address")

    args.out.mkdir(parents=True, exist_ok=True)
    qr = segno.make(args.url, error="q")
    for ext, scale in (("png", 20), ("svg", 10)):
        path = args.out / f"{args.name}-qr.{ext}"
        qr.save(path, scale=scale, border=4)
        print(f"Saved {path}")

    svg, w, h = poster_svg(qr, args.url)
    svg_path = args.out / f"{args.name}-scan-me.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Saved {svg_path}")
    png_path = args.out / f"{args.name}-scan-me.png"
    if render_png(svg, png_path, 2 * w, 2 * h):
        print(f"Saved {png_path}")
    else:
        print("Poster PNG skipped: Microsoft Edge not found (the SVG is complete)")


if __name__ == "__main__":
    main()
