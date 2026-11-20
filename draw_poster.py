#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster (1024x1024 PNG).

Renders a clean newspaper front page with PIL and DejaVu fonts: a masthead
with the date, six story panels across justice, diplomacy, war, the Gulf,
markets and weather, and a footer of two more briefs. All text is drawn by
this script, so it stays crisp and legible at small sizes.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 42, 71)
GOLD = (242, 183, 5)
INK = (24, 24, 24)
GREY = (74, 74, 74)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_TITLE = font("DejaVuSans-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 58)
F_SUB = font("DejaVuSans.ttf", 21)
F_TAG = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 19)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 19)

STORIES = [
    ("JUSTICE  ·  THE HAGUE", (106, 27, 154),
     "World Court: Myanmar committed genocide",
     "ICJ rules 9–6 — a first against a state — over the 2017 attacks on the "
     "Rohingya. 1.3 million remain displaced."),
    ("SUMMIT  ·  SHENZHEN", (11, 110, 79),
     "Trump, Xi and Putin in first three-way summit",
     "70 minutes of talks end in a four-point declaration on nuclear risk "
     "and energy. No mention of Ukraine or Iran."),
    ("WAR  ·  KYIV", (183, 28, 28),
     "Russia strikes Kyiv overnight; 8 killed",
     "Missiles and drones hit bridges; 28 people hurt. Two missiles and a "
     "drone crossed into Poland."),
    ("GULF  ·  RIYADH", (140, 110, 0),
     "Houthi missile hits Riyadh's PIF Tower",
     "Saudi wealth-fund tower damaged in the financial district. No injuries "
     "reported."),
    ("MARKETS  ·  NEW YORK", (21, 101, 192),
     "Anthropic's $81bn debut; stocks slide",
     "Shares close 17% up at ~$97 on Nasdaq. The S&P falls a fifth day; "
     "Japan's Nikkei drops 4.8%."),
    ("WEATHER  ·  ODISHA", (0, 131, 143),
     "Cyclone Akvan hits India's east coast",
     "Landfall near Gopalpur with 80 km/h winds. More than 300,000 people "
     "evacuated."),
]


def wrap(draw, text, fnt, width):
    """Wrap text to fit width, returning lines (max 3 for headlines, 4 body)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.text((36, 22), "WORLD NEWS", font=F_TITLE, fill=WHITE)
    d.text((36, 88), "20 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    # Small globe mark, top right.
    d.ellipse([868, 30, 988, 150], outline=GOLD, width=5)
    d.ellipse([898, 60, 958, 120], fill=GOLD)
    d.text((700, 34), "FRIDAY", font=F_TAG, fill=WHITE)
    d.text((700, 62), "THE DAY IN", font=F_TAG, fill=WHITE)
    d.text((700, 90), "SIX STORIES", font=F_TAG, fill=WHITE)

    # Sub strip.
    d.rectangle([0, 168, W, 206], fill=(232, 224, 204))
    sub = "Six stories that defined the day — The Hague · Shenzhen · Kyiv · Riyadh · New York · Odisha"
    d.text(((W - d.textlength(sub, font=F_SUB)) / 2, 176), sub, font=F_SUB, fill=NAVY)

    # Story grid: 2 columns x 3 rows.
    px, py, pw, ph, gap = 36, 220, 472, 224, 16
    for i, (tag, colour, headline, body) in enumerate(STORIES):
        x = px + (i % 2) * (pw + gap)
        y = py + (i // 2) * (ph + gap)
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=10, fill=WHITE,
                            outline=(210, 200, 180), width=1)
        d.rectangle([x, y, x + 10, y + ph], fill=colour)
        tx = x + 26
        d.text((tx, y + 14), tag, font=F_TAG, fill=colour)
        lines = wrap(d, headline, F_HEAD, pw - 44)[:2]
        ly = y + 44
        for line in lines:
            d.text((tx, ly), line, font=F_HEAD, fill=NAVY)
            ly += 32
        blines = wrap(d, body, F_BODY, pw - 44)[:3]
        ly += 6
        for line in blines:
            d.text((tx, ly), line, font=F_BODY, fill=GREY)
            ly += 26

    # Footer briefs.
    d.rectangle([0, 936, W, H], fill=NAVY)
    d.text((36, 950), "ALSO:", font=F_FOOT_B, fill=GOLD)
    foot = ("Kenya — last Ebola patient discharged, 42-day countdown to all-clear.   "
            "Gaza — Israeli troops cross the Yellow Line in first incursion since the truce.")
    flines = wrap(d, foot, F_FOOT, W - 110 - 36)
    ly = 950
    for line in flines[:2]:
        d.text((110, ly), line, font=F_FOOT, fill=WHITE)
        ly += 24

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
