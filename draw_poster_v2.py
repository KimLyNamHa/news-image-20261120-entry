#!/usr/bin/env python3
"""Draw the v2 world-news poster for Friday 20 November 2026 (1024x1024 PNG).

Original work, drawn programmatically with PIL and DejaVu fonts. Layout is
deliberately a little random, not a uniform grid: one wide lead (Kyiv), a
narrower cyclone lead and a narrow markets lead; card rows of 4, 3 and 3 with
uneven widths; a timeline ribbon that arcs the day from overnight Kyiv, to
the 08:30 Akvan landfall, to the Asian market close. The masthead, stat bar,
region bar, world map, 22-story also-list and red DATE CHECK box are kept.

35 stories in all: 3 leads + 10 cards + 22 briefs. Every story happened, or
was first reported, on Friday 20 November 2026; sources are named beside
each story. Thursday 19 November stories are NOT shown as Friday news:
the World Court ruling on Myanmar, the three-leader declaration in
Shenzhen, Anthropic's $83 IPO pricing and Nasdaq debut, the Houthi strike
on Riyadh's PIF Tower, the GTA VI midnight launch and the $190.4m Van
Gogh sale are listed only in the DATE CHECK box as excluded.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 42, 71)
NIGHT = (10, 28, 58)
RED = (178, 28, 28)
GOLD = (242, 183, 5)
INK = (24, 24, 24)
GREY = (74, 74, 74)
WHITE = (255, 255, 255)
TEAL = (0, 110, 120)
GREEN = (30, 110, 60)
BLUE = (21, 80, 160)
PURPLE = (106, 27, 154)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size, fallback="DejaVuSans.ttf"):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.truetype(FONT_DIR + fallback, size)


F_SERIF = font("DejaVuSerif-Bold.ttf", 58)
F_SERIF_SM = font("DejaVuSerif.ttf", 17)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 11)
F_STAT = font("DejaVuSans-Bold.ttf", 25)
F_STAT_L = font("DejaVuSans.ttf", 11)
F_TAG = font("DejaVuSans-Bold.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_BODY = font("DejaVuSans.ttf", 13)
F_CARD_H = font("DejaVuSans-Bold.ttf", 15)
F_CARD_B = font("DejaVuSans.ttf", 12)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 11)
F_SMALL = font("DejaVuSans.ttf", 11)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 11)
F_NUM = font("DejaVuSans-Bold.ttf", 10)


def wrap(d, text, fnt, width, max_lines=None):
    """Wrap text to pixel width; truncate the last line with an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " ...", font=fnt) > width:
            lines[-1] = lines[-1][:-1].strip()
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def one_line(d, text, fnt, width):
    """Fit text to one line, truncating with an ellipsis if needed."""
    if d.textlength(text, font=fnt) <= width:
        return text
    while text and d.textlength(text + "...", font=fnt) > width:
        text = text[:-1].rstrip()
    return text + "..."


def card(d, x, y, w, h, tag, headline, body, colour):
    """A text card under its illustration banner; tag already holds its number."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=WHITE,
                        outline=(205, 195, 175), width=1)
    d.text((x + 10, y + 6), tag, font=F_TAG, fill=colour)
    ly = y + 24
    for line in wrap(d, headline, F_CARD_H, w - 20, 2):
        d.text((x + 10, ly), line, font=F_CARD_H, fill=NAVY)
        ly += 17
    ly += 2
    for line in wrap(d, body, F_CARD_B, w - 20, 2):
        d.text((x + 10, ly), line, font=F_CARD_B, fill=GREY)
        ly += 13


# ------------------------------------------------------------------ art
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(20, 12), (70, 26), (150, 8), (230, 22), (300, 10),
                   (360, 28), (110, 38), (260, 40)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    for (x0, y0, x1, y1) in [(40, 4, 120, 52), (180, 2, 250, 56),
                             (320, 6, 360, 50)]:
        for t in range(0, 11):
            px = x + x0 + (x1 - x0) * t / 10
            py = y + y0 + (y1 - y0) * t / 10 + 12 * math.sin(math.pi * t / 10)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
    d.rectangle([x, y + h - 22, x + w, y + h - 17], fill=(120, 130, 150))
    for cx in (70, 200, 330):
        d.arc([x + cx - 46, y + h - 52, x + cx + 46, y + h - 4],
              180, 360, fill=(150, 160, 180), width=3)
        d.line([x + cx - 46, y + h - 18, x + cx - 46, y + h - 52],
               fill=(150, 160, 180), width=3)
        d.line([x + cx + 46, y + h - 18, x + cx + 46, y + h - 52],
               fill=(150, 160, 180), width=3)
    for bx, by, r in [(120, h - 30, 11), (250, h - 27, 8), (350, h - 32, 10)]:
        d.ellipse([x + bx - r, y + by - r, x + bx + r, y + by + r],
                  fill=(255, 170, 40))
        d.ellipse([x + bx - r // 2, y + by - r // 2, x + bx + r // 2,
                   y + by + r // 2], fill=(255, 230, 120))
    for bx, bw, bh in [(10, 26, 30), (300, 22, 24), (380, 18, 20)]:
        d.rectangle([x + bx, y + h - 22 - bh, x + bx + bw, y + h - 22],
                    fill=(30, 55, 90))


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 110, 160))
    d.polygon([(x, y), (x + 62, y), (x + 48, y + h // 2), (x + 70, y + h),
               (x, y + h)], fill=(214, 196, 150))
    d.ellipse([x + 44, y + h - 30, x + 52, y + h - 22], fill=RED)
    d.text((x + 8, y + h - 18), "GOPALPUR", font=F_SMALL_B, fill=NAVY)
    cx, cy = x + w - 92, y + h // 2 - 4
    for r, col in [(56, (255, 255, 255)), (44, (180, 220, 240)),
                   (32, (255, 255, 255)), (20, (180, 220, 240)),
                   (10, (255, 255, 255))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 320, fill=col, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    for rx in range(0, w, 26):
        d.line([x + rx, y + 6, x + rx - 8, y + 22], fill=(200, 225, 240),
               width=2)


def art_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 16, 16))
    for gy in range(1, 4):
        yy = y + h * gy // 4
        d.line([x + 6, yy, x + w - 6, yy], fill=(50, 50, 50), width=1)
    pts = [(x + 10, y + 12), (x + 60, y + 26), (x + 110, y + 22),
           (x + 160, y + 44), (x + 210, y + 52), (x + 260, y + 72)]
    d.line(pts, fill=(255, 70, 70), width=3, joint="curve")
    for (cx, top, bot) in [(40, 16, 30), (90, 30, 42), (140, 26, 40),
                           (190, 48, 62), (240, 56, 70)]:
        d.rectangle([x + cx - 5, y + top, x + cx + 5, y + bot],
                    fill=(200, 40, 40))
    d.text((x + 10, y + h - 20), "TAIPEI -6.2%", font=F_SMALL_B, fill=WHITE)
    d.text((x + 108, y + h - 20), "SEOUL -5.2%", font=F_SMALL_B,
           fill=(255, 120, 120))
    d.text((x + 206, y + h - 20), "TOKYO -4.8%", font=F_SMALL_B, fill=WHITE)


def art_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 232, 240))
    cx, cy, r = x + 42, y + h // 2, 22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 120, 180))
    d.ellipse([cx - 12, cy - 14, cx + 4, cy - 2], fill=(90, 170, 90))
    d.ellipse([cx - 2, cy + 4, cx + 14, cy + 16], fill=(90, 170, 90))
    d.rounded_rectangle([x + w - 32, y + 6, x + w - 22, y + h - 12],
                        radius=5, fill=WHITE, outline=RED, width=2)
    d.rectangle([x + w - 29, y + h - 22, x + w - 25, y + h - 14], fill=RED)
    d.ellipse([x + w - 34, y + h - 20, x + w - 20, y + h - 6], fill=RED)


def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w // 2 - 2, y + h], fill=NAVY)
    d.line([x, y, x + w // 2 - 2, y + h], fill=WHITE, width=5)
    d.line([x, y + h, x + w // 2 - 2, y], fill=WHITE, width=5)
    d.line([x + w // 4, y, x + w // 4, y + h], fill=WHITE, width=7)
    d.line([x, y + h // 2, x + w // 2 - 2, y + h // 2], fill=WHITE, width=7)
    d.line([x + w // 4, y, x + w // 4, y + h], fill=RED, width=3)
    d.line([x, y + h // 2, x + w // 2 - 2, y + h // 2], fill=RED, width=3)
    ex = x + w // 2 + 2
    d.rectangle([ex, y, x + w, y + h], fill=(0, 50, 140))
    for k in range(12):
        a = 2 * math.pi * k / 12
        sx = ex + (w // 2) // 2 + int(15 * math.cos(a))
        sy = y + h // 2 + int(13 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def art_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 170))
    d.line([x + 8, y + h - 10, x + w - 8, y + 10], fill=GREY, width=2)
    mx, my = x + w // 2, y + h // 2
    d.polygon([(mx - 34, my + 6), (mx + 22, my - 8), (mx + 34, my - 2),
               (mx + 22, my + 8)], fill=(90, 95, 100))
    d.polygon([(mx - 34, my + 6), (mx - 44, my + 12), (mx - 40, my + 2)],
              fill=(255, 140, 40))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 140, 90))


def art_convoy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 204, 150))
    d.ellipse([x + w - 32, y + 5, x + w - 10, y + 27], fill=(255, 190, 80))
    for vx in (14, 62, 110, 158):
        d.rectangle([x + vx, y + h - 30, x + vx + 34, y + h - 14],
                    fill=(70, 70, 70))
        d.rectangle([x + vx + 6, y + h - 38, x + vx + 26, y + h - 30],
                    fill=(100, 100, 100))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(160, 130, 80))


def art_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w // 3, y + h], fill=GREEN)
    d.rectangle([x + w // 3, y, x + 2 * w // 3, y + h], fill=WHITE)
    d.rectangle([x + 2 * w // 3, y, x + w, y + h], fill=RED)
    for px in range(16, w - 10, 22):
        d.ellipse([x + px, y + h - 20, x + px + 9, y + h - 11], fill=INK)
        d.rectangle([x + px + 2, y + h - 10, x + px + 7, y + h - 3],
                    fill=INK)


def art_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    d.ellipse([x + 16, y + 6, x + 42, y + 32], fill=RED)
    bars = [(70, 10), (100, 16), (130, 22), (160, 28)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 8 - bh, x + bx + 20, y + h - 8],
                    fill=NAVY)
    d.line([x + 60, y + h - 10, x + 190, y + h - 10], fill=GREY, width=2)


def art_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 20))
    for sx, sy in [(16, 8), (60, 22), (120, 6), (200, 16), (280, 10),
                   (330, 24), (90, 34), (240, 36)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    cx, cy, r = x + w - 62, y + h // 2, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 165, 155))
    for ox, oy, orad in [(-8, -6, 4), (6, 5, 3), (-2, 10, 2)]:
        d.ellipse([cx + ox - orad, cy + oy - orad, cx + ox + orad,
                   cy + oy + orad], fill=(130, 125, 115))
    d.rectangle([x + 30, y + h // 2 - 7, x + 50, y + h // 2 + 7],
                fill=(200, 200, 210))
    d.rectangle([x + 10, y + h // 2 - 4, x + 30, y + h // 2 + 4],
                fill=(40, 90, 180))
    d.rectangle([x + 50, y + h // 2 - 4, x + 70, y + h // 2 + 4],
                fill=(40, 90, 180))
    for t in range(0, 11):
        px = x + 76 + (cx - r - 84) * t / 10
        py = y + h // 2 - 5 * math.sin(math.pi * t / 10)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)


def art_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 20, 20))
    f20 = font("DejaVuSans-Bold.ttf", 20)
    d.text((x + 12, y + 4), "3.00%", font=f20, fill=WHITE)
    d.text((x + 96, y + 4), "3.50%", font=f20, fill=GOLD)
    d.text((x + 12, y + 30), "18TH MONTH ON HOLD", font=F_SMALL_B,
           fill=WHITE)


def art_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 190, 90))
    d.ellipse([x + w - 48, y + 5, x + w - 16, y + 37], fill=(255, 220, 120))
    bx = x + 40
    d.polygon([(bx, y + h - 10), (bx + 18, y + 8), (bx + 36, y + h - 10)],
              outline=INK, width=3)
    d.line([bx + 9, y + h - 22, bx + 27, y + h - 22], fill=INK, width=2)
    d.line([bx + 18, y + 8, bx + 18, y], fill=INK, width=3)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 80, 40))


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
    d.rectangle([x + w // 2 - 60, y, x + w // 2 + 60, y + h],
                fill=(214, 190, 140))
    for sx in (w // 2 - 12, w // 2, w // 2 + 12):
        d.line([x + sx, y + 8, x + sx, y + 22], fill=(255, 230, 160), width=3)
    d.polygon([(x + 30, y + h - 12), (x + 44, y + h - 20),
               (x + 96, y + 18), (x + 84, y + 26)], fill=(150, 100, 50))
    d.polygon([(x + 96, y + 18), (x + 104, y + 10), (x + 112, y + 16),
               (x + 104, y + 24)], fill=(120, 80, 40))
    d.ellipse([x + w - 30, y + 12, x + w - 16, y + 26], fill=RED)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.polygon([(x + 18, y + 30), (x + 52, y + 18), (x + 88, y + 26),
               (x + 80, y + 48), (x + 48, y + 54), (x + 22, y + 46)],
              fill=(214, 196, 150))
    d.polygon([(x + 62, y + 62), (x + 84, y + 58), (x + 92, y + 80),
               (x + 78, y + 100), (x + 64, y + 84)], fill=(214, 196, 150))
    d.polygon([(x + 128, y + 26), (x + 158, y + 18), (x + 176, y + 30),
               (x + 162, y + 44), (x + 136, y + 42)], fill=(214, 196, 150))
    d.polygon([(x + 140, y + 52), (x + 168, y + 48), (x + 178, y + 70),
               (x + 162, y + 94), (x + 146, y + 76)], fill=(214, 196, 150))
    d.polygon([(x + 184, y + 24), (x + 252, y + 16), (x + 282, y + 32),
               (x + 268, y + 58), (x + 220, y + 62), (x + 192, y + 48)],
              fill=(214, 196, 150))
    d.polygon([(x + 262, y + 92), (x + 282, y + 88), (x + 288, y + 102),
               (x + 272, y + 108), (x + 260, y + 102)],
              fill=(214, 196, 150))
    pins = {1: (158, 30), 2: (238, 54), 3: (252, 36), 4: (168, 26),
            5: (140, 28), 6: (162, 34), 7: (180, 40), 8: (148, 38),
            9: (262, 32), 11: (226, 36), 12: (168, 62), 13: (282, 100)}
    for n, (px, py) in pins.items():
        d.ellipse([x + px - 7, y + py - 7, x + px + 7, y + py + 7],
                  fill=RED, outline=WHITE, width=1)
        d.text((x + px - 3, y + py - 6), str(n), font=F_NUM, fill=WHITE)
    d.text((x + 10, y + h - 34), "Pins 1-13 mark the lead & card stories.",
           font=F_SMALL, fill=(200, 205, 215))
    d.text((x + 10, y + h - 20), "10 · SPACE — MERCURY, ABOVE",
           font=F_SMALL_B, fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Masthead.
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((8, 12), "THE WORLD IN ONE DAY", font=F_KICK, fill=RED)
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    d.text((W - 8 - d.textlength(right, font=F_KICK_SM), 14), right,
           font=F_KICK_SM, fill=GREY)
    d.text((8, 30), "Friday 20 November 2026", font=F_SERIF, fill=NAVY)
    d.text((8, 92), "Missiles hit Kyiv's bridges · Cyclone Akvan lands in India · "
           "Asia's markets sink in the AI sell-off", font=F_SERIF_SM,
           fill=GREY)
    d.line([8, 114, W - 8, 114], fill=NAVY, width=2)

    # --- Timeline ribbon: the day's arc, overnight to market close.
    d.text((8, 120), "OVERNIGHT — KYIV", font=F_SMALL_B, fill=NAVY)
    d.text((330, 120), "→  08:30 — GOPALPUR", font=F_SMALL_B, fill=TEAL)
    d.text((620, 120), "→  CLOSE — TAIPEI · SEOUL · TOKYO", font=F_SMALL_B,
           fill=RED)

    # --- Stat bar, uneven cells.
    stats = [
        ("3", "bridges hit in Kyiv", NAVY, 148),
        ("300,000+", "moved before Akvan", NAVY, 168),
        ("-6.2%", "Taiex — worst week since 1991", RED, 196),
        ("100,000", "youth visas a year, UK–EU deal", NAVY, 168),
        ("2.3%", "Japan inflation, Oct", NAVY, 148),
        ("118", "Phillips v India", NAVY, 180),
    ]
    sx = 8
    for num, label, col, w in stats:
        d.line([sx, 138, sx, 188], fill=(200, 190, 170), width=1)
        d.text((sx + 8, 136), num, font=F_STAT, fill=col)
        ly = 166
        for line in wrap(d, label, F_STAT_L, w - 14, 2):
            d.text((sx + 8, ly), line, font=F_STAT_L, fill=GREY)
            ly += 12
        sx += w
    d.line([8, 194, W - 8, 194], fill=(200, 190, 170), width=1)

    # --- Region bar.
    regions = [("EUROPE 9", 9, RED), ("ASIA 7", 7, TEAL),
               ("MIDEAST 3", 3, (180, 140, 0)), ("AFRICA 6", 6, GREEN),
               ("AMERICAS 4", 4, BLUE), ("OCEANIA 3", 3, PURPLE),
               ("GLOBAL 3", 3, GREY)]
    rx = 8
    total = sum(n for _, n, _ in regions)
    for name, n, col in regions:
        w = int(1008 * n / total)
        d.rectangle([rx, 198, rx + w - 2, 212], fill=col)
        d.text((rx + 5, 201), name, font=F_SMALL_B, fill=WHITE)
        rx += w

    # --- Leads: one wide, one mid, one narrow.
    leads = [
        (8, 404, art_kyiv, "1 · KYIV, UKRAINE · WAR",
         "Russian missiles hit three Kyiv bridges",
         "Overnight barrage of ~110 missiles and 400 drones kills 3 in "
         "Kyiv. (Reuters)"),
        (420, 296, art_cyclone, "2 · ODISHA, INDIA · CYCLONE",
         "Cyclone Akvan comes ashore in eastern India",
         "Landfall near Gopalpur at 08:30; 300,000+ in shelters. (IMD)"),
        (724, 292, art_chart, "3 · TAIPEI · SEOUL · TOKYO · MARKETS",
         "AI sell-off sinks Asia's stock markets",
         "Taiex falls 6.2%, worst week since 1991. (Reuters)"),
    ]
    for x, w, art, tag, head, body in leads:
        y0 = 218
        art(d, x, y0, w, 80)
        d.text((x, y0 + 86), tag, font=F_TAG, fill=RED)
        ly = y0 + 104
        for line in wrap(d, head, F_HEAD, w - 4, 2):
            d.text((x, ly), line, font=F_HEAD, fill=NAVY)
            ly += 24
        for line in wrap(d, body, F_BODY, w - 4, 2):
            d.text((x, ly), line, font=F_BODY, fill=GREY)
            ly += 16

    # --- Card rows: 4, then 3, then 3, all with uneven widths.
    rows = [
        (402, [
            (8, 250, art_globe, "4 · ANTALYA · CLIMATE",
             "COP31 reaches its last day with no deal",
             "Draft drops fossil fuels. (UN News)", RED),
            (266, 300, art_flags, "5 · BRUSSELS · DIPLOMACY",
             "UK and EU seal a 'reset' deal",
             "Youth visas, food trade, carbon link. (Reuters)", NAVY),
            (574, 200, art_missile, "6 · POLAND · SECURITY",
             "Russian missile lands in Poland",
             "Kh-101 falls in a field. (Reuters)", RED),
            (782, 234, art_convoy, "7 · CENTRAL IRAQ · SECURITY",
             "Iraqi army enters a militia stronghold",
             "Troops deploy in Jurf al-Sakhar under a deal. (Reuters)",
             NAVY),
        ]),
        (528, [
            (8, 340, art_italy, "8 · ITALY · LABOUR",
             "General strike over Italy's budget",
             "CGIL stops work for a day; marches in 100+ cities. (Reuters)",
             RED),
            (356, 300, art_japan, "9 · TOKYO · ECONOMY",
             "Japan's inflation picks up to 2.3%",
             "Headline CPI 2.3% in Oct; core 2.2%. (Reuters)", NAVY),
            (664, 352, art_space, "10 · MERCURY · SPACE",
             "BepiColombo arrives at Mercury",
             "After 8 years, orbit burn set for Saturday. (ESA)", NAVY),
        ]),
        (654, [
            (8, 240, art_china, "11 · BEIJING · RATES",
             "China holds lending rates",
             "1-yr 3.00%, 5-yr 3.50% — 18th month on hold. (PBOC)", RED),
            (256, 330, art_kenya, "12 · TURKANA, KENYA · ENERGY",
             "Kenya starts drilling its first oil well",
             "Spudding at Amosing; first oil due 1 Dec. (Capital FM)",
             GREEN),
            (594, 422, art_cricket, "13 · WELLINGTON · CRICKET",
             "Phillips hits 118 against India",
             "His 118, with Nicholls' 175*, lifts NZ to 368. (Reuters)",
             GREEN),
        ]),
    ]
    for y0, cards in rows:
        for x, w, art, tag, head, body, col in cards:
            art(d, x, y0, w, 48)
            card(d, x, y0 + 48, w, 80, tag, head, body, col)

    # --- Map + also-list.
    yM = 790
    d.text((8, yM), "WHERE IT HAPPENED", font=F_KICK, fill=NAVY)
    draw_map(d, 8, yM + 16, 296, 130)
    d.text((312, yM), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES",
           font=F_KICK, fill=RED)
    briefs = [
        (14, "Bukele registers for a third term. (Reuters)"),
        (15, "Senegal boat capsizes; 4 bodies found. (Al Jazeera)"),
        (16, "Pill + chemo shrinks tumours in 60.7%. (EORTC)"),
        (17, "Strike on a Lviv railway station kills two. (BBC)"),
        (18, "SoftBank shares fall 14% in a day. (Al Jazeera)"),
        (19, "KOSPI ends the week 7.9% lower. (Anadolu)"),
        (20, "209 mm of rain as Akvan crosses Odisha. (PTI)"),
        (21, "Israeli strikes hit Lebanon's south. (Anadolu)"),
        (22, "Gunmen fire on a cargo ship off Yemen. (UKMTO)"),
        (23, "Court bars new evidence against Tinubu. (Channels TV)"),
        (24, "Police to enforce Ebola ban on rallies. (allAfrica)"),
        (25, "Fuel crisis brings night petrol queues. (Al Jazeera)"),
        (26, "AFDB: 22 countries are in debt distress. (allAfrica)"),
        (27, "Russell fastest in wet GP practice. (Formula1.com)"),
        (28, "Nasdaq futures fall 1.6% pre-bell. (24/7 Wall St)"),
        (29, "Democrats query a law firm's free work. (Al Jazeera)"),
        (30, "Nicholls makes 175 in a 216-run stand. (ICC)"),
        (31, "Australian shares fall 1.8%. (Reuters)"),
        (32, "Panama asks COP31 to cap world oil output. (Anadolu)"),
        (33, "EU official calls draft unacceptable. (RTE)"),
        (34, "ATP backs plan to lift player pay past $350m. (Anadolu)"),
        (35, "General says UK runs cyber attacks abroad. (Sky News)"),
    ]
    for cx, items in [(312, briefs[:11]), (668, briefs[11:])]:
        ly = yM + 18
        for n, text in items:
            num = f"{n}  "
            d.text((cx, ly), num, font=F_BRIEF_B, fill=RED)
            tw = d.textlength(num, font=F_BRIEF_B)
            line = one_line(d, text, F_BRIEF, 348 - tw)
            d.text((cx + tw, ly), line, font=F_BRIEF, fill=INK)
            ly += 12

    # --- Date check.
    d.rectangle([8, 958, W - 8, 990], outline=RED, width=2)
    d.text((16, 964), "DATE CHECK", font=F_SMALL_B, fill=RED)
    dc = ("Left out as Thursday 19 Nov news: World Court ruling on Myanmar; "
          "three-leader Shenzhen declaration; Anthropic's $83 IPO pricing; "
          "Houthi strike on Riyadh's PIF Tower; GTA VI launch; $190.4m "
          "Van Gogh sale.")
    ly = 964
    for line in wrap(d, dc, F_SMALL, W - 8 - 16 - 100, 2):
        d.text((116, ly), line, font=F_SMALL, fill=INK)
        ly += 13

    # --- Footer.
    foot = ("Every story here happened, or was first reported, on Friday 20 "
            "November 2026. Sources named beside each story · Original drawings")
    d.text(((W - d.textlength(foot, font=F_SMALL)) / 2, 998), foot,
           font=F_SMALL, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
