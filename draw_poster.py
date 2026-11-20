#!/usr/bin/env python3
"""Draw the news poster for 20 November 2026.

One 1024x1024 image, six stories from the brief, drawn with Pillow shapes
and DejaVu fonts. Run: python3 draw_poster.py  -> writes entry.png next
to this file.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (12, 26, 43)
PANEL = (21, 42, 66)
PANEL_EDGE = (38, 66, 102)
INK = (242, 245, 248)
MUTED = (169, 184, 201)
SUB = (199, 211, 224)
GOLD = (232, 184, 75)
RED = (228, 87, 75)
TEAL = (63, 182, 178)
BLUE = (91, 141, 239)
GREEN = (76, 175, 125)
PURPLE = (155, 126, 222)
WHITE = (255, 255, 255)
DARK = (16, 28, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_star(d, cx, cy, r, color):
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=color, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=color)


def icon_calendar(d, cx, cy):
    d.rounded_rectangle([cx - 50, cy - 54, cx + 50, cy + 54], radius=10,
                        fill=WHITE, outline=GOLD, width=3)
    d.rounded_rectangle([cx - 50, cy - 54, cx + 50, cy - 20], radius=10,
                        fill=RED)
    d.rectangle([cx - 50, cy - 30, cx + 50, cy - 20], fill=RED)
    for dx in (-28, 28):
        d.line([(cx + dx, cy - 64), (cx + dx, cy - 44)], fill=GOLD, width=5)
    f = font(SANS_BOLD, 27)
    d.text((cx, cy + 12), "2027", font=f, fill=DARK, anchor="mm")
    d.ellipse([cx - 16, cy + 26, cx + 16, cy + 58], outline=GOLD, width=3)
    d.line([(cx, cy + 42), (cx, cy + 32)], fill=GOLD, width=3)
    d.line([(cx, cy + 42), (cx + 8, cy + 46)], fill=GOLD, width=3)


def icon_scales(d, cx, cy):
    d.line([(cx, cy - 56), (cx, cy + 44)], fill=GOLD, width=5)
    d.line([(cx - 46, cy - 48), (cx + 46, cy - 48)], fill=GOLD, width=5)
    d.line([(cx - 20, cy + 52), (cx + 20, cy + 52)], fill=GOLD, width=5)
    d.ellipse([cx - 5, cy - 62, cx + 5, cy - 52], fill=GOLD)
    for sx in (-46, 46):
        px = cx + sx
        d.line([(px, cy - 48), (px - 18, cy - 6)], fill=GOLD, width=3)
        d.line([(px, cy - 48), (px + 18, cy - 6)], fill=GOLD, width=3)
        d.line([(px, cy - 48), (px, cy - 6)], fill=GOLD, width=3)
        d.pieslice([px - 18, cy - 14, px + 18, cy + 14], 0, 180, fill=GOLD)
    d.line([(cx, cy + 44), (cx, cy + 52)], fill=GOLD, width=5)


def icon_voyager(d, cx, cy):
    d.arc([cx - 70, cy - 70, cx + 70, cy + 70], 200, 330, fill=BLUE, width=3)
    draw_star(d, cx + 52, cy - 44, 7, WHITE)
    draw_star(d, cx - 58, cy + 18, 5, WHITE)
    draw_star(d, cx + 40, cy + 52, 5, WHITE)
    d.polygon([(cx - 44, cy - 26), (cx + 6, cy - 44), (cx + 44, cy + 6),
               (cx - 6, cy + 22)], fill=GOLD, outline=WHITE)
    d.rectangle([cx - 26, cy + 8, cx + 2, cy + 30], fill=(200, 170, 80),
                outline=WHITE)
    d.line([(cx - 12, cy + 19), (cx - 34, cy + 52)], fill=WHITE, width=3)
    d.line([(cx + 30, cy - 20), (cx + 48, cy - 38)], fill=WHITE, width=3)
    d.ellipse([cx + 44, cy - 42, cx + 52, cy - 34], fill=RED)


def icon_cyclone(d, cx, cy):
    for i, r in enumerate((14, 24, 34, 44, 54)):
        start = 20 + i * 55
        d.arc([cx - r, cy - 14 - r, cx + r, cy - 14 + r], start, start + 250,
              fill=TEAL, width=5)
    for dx, dy in ((-30, 52), (0, 60), (30, 52)):
        d.polygon([(cx + dx, cy + dy - 12), (cx + dx - 6, cy + dy + 4),
                   (cx + dx + 6, cy + dy + 4)], fill=TEAL)
        d.ellipse([cx + dx - 6, cy + dy - 2, cx + dx + 6, cy + dy + 10],
                  fill=TEAL)


def icon_gta(d, cx, cy):
    f = font(SERIF_BOLD, 62)
    d.text((cx, cy - 34), "VI", font=f, fill=GOLD, anchor="mm")
    d.rectangle([cx - 44, cy + 6, cx - 12, cy + 52], fill=GREEN)
    d.rectangle([cx + 12, cy + 22, cx + 44, cy + 52], fill=(120, 130, 145))
    f2 = font(SANS_BOLD, 13)
    d.text((cx - 28, cy + 64), "GTA 6", font=f2, fill=GREEN, anchor="mm")
    d.text((cx + 28, cy + 64), "FILM", font=f2, fill=MUTED, anchor="mm")


def icon_hayabusa(d, cx, cy):
    pts = [(cx - 52, cy - 10), (cx - 30, cy - 44), (cx + 8, cy - 50),
           (cx + 42, cy - 28), (cx + 50, cy + 8), (cx + 22, cy + 38),
           (cx - 18, cy + 44), (cx - 48, cy + 22)]
    d.polygon(pts, fill=(138, 151, 165), outline=(200, 210, 220))
    for ox, oy, r in ((-18, -18, 7), (14, 6, 9), (-6, 22, 5)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  fill=(110, 122, 136))
    px, py = cx + 34, cy - 46
    d.rectangle([px - 8, py - 6, px + 8, py + 6], fill=WHITE)
    d.rectangle([px - 26, py - 4, px - 10, py + 4], fill=BLUE)
    d.rectangle([px + 10, py - 4, px + 28, py + 4], fill=BLUE)
    d.line([(px - 14, py + 34), (px + 14, py + 62)], fill=RED, width=6)
    d.line([(px + 14, py + 34), (px - 14, py + 62)], fill=RED, width=6)


STORIES = [
    ("WORLD", "Trump delays Iran war call to 2027",
     "\u2018See what happens\u2019 after 1 January \u2014 no rush to decide.",
     GOLD, icon_calendar),
    ("JUSTICE", "ICJ: Myanmar committed genocide",
     "UN court: army meant to destroy the Rohingya in 2017.",
     RED, icon_scales),
    ("SPACE", "Voyager 1 reaches one light-day",
     "NASA confirms the milestone, ~50 years after launch.",
     BLUE, icon_voyager),
    ("WEATHER", "Cyclone Akvan hits Odisha",
     "300,000 evacuated; 423 rescue teams on standby.",
     TEAL, icon_cyclone),
    ("GAMES", "GTA 6 outsells The Odyssey",
     "Sales pass $1.80 billion at the global box office.",
     GREEN, icon_gta),
    ("SPACE", "Hayabusa2 landing called off",
     "Engine trouble forces Japan to scrap asteroid touchdown.",
     PURPLE, icon_hayabusa),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead.
    title_f = font(SERIF_BOLD, 54)
    d.text((W // 2, 52), "THE WORLD IN ONE DAY", font=title_f, fill=INK,
           anchor="mm")
    date_f = font(SANS_BOLD, 30)
    d.text((W // 2, 106), "FRIDAY  \u00b7  20 NOVEMBER 2026", font=date_f,
           fill=GOLD, anchor="mm")
    d.line([(72, 140), (W - 72, 140)], fill=GOLD, width=3)

    # Story grid: 2 columns x 3 rows.
    margin, gap = 24, 16
    col_w = (W - 2 * margin - gap) // 2
    row_h = 258
    top = 164
    tag_f = font(SANS_BOLD, 16)
    head_f = font(SANS_BOLD, 27)
    sub_f = font(SANS, 19)

    for idx, (tag, head, sub, accent, icon) in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x0 = margin + col * (col_w + gap)
        y0 = top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=PANEL,
                            outline=accent, width=3)
        icon(d, x0 + 78, y0 + row_h // 2)
        d.line([(x0 + 156, y0 + 22), (x0 + 156, y1 - 22)],
               fill=PANEL_EDGE, width=2)
        tx = x0 + 172
        text_w = x1 - 16 - tx
        d.text((tx, y0 + 26), tag, font=tag_f, fill=accent)
        lines = wrap(d, head, head_f, text_w)
        y = y0 + 52
        for line in lines:
            d.text((tx, y), line, font=head_f, fill=INK)
            y += 33
        y += 6
        for line in wrap(d, sub, sub_f, text_w):
            d.text((tx, y), line, font=sub_f, fill=SUB)
            y += 25

    # Footer.
    foot_f = font(SANS_BOLD, 17)
    d.text((W // 2, 994), "SIX STORIES  \u00b7  ONE DAY  \u00b7  20 NOVEMBER 2026",
           font=foot_f, fill=MUTED, anchor="mm")

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"entry.png: {img.size[0]}x{img.size[1]}, {size} bytes, sha256 {sha}")
    assert size <= 1048576, "image over 1 MiB"


if __name__ == "__main__":
    main()
