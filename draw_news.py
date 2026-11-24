#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Stories verified by web news search on 2026-11-24 (JST afternoon):
lead NATO AWACS to Poland (Reuters, 24 Nov) + overnight Russian drone
incursion into Polish airspace; Korea airspace incursions; Ukraine sinking
a Russian warship off Libya; Nvidia reinstates Jensen Huang; Democrats'
record House majority; Zanzibar hotel fire; Honda airbag recall.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 38, 30)
GREY = (90, 86, 78)
LINE = (200, 192, 175)
CARD = (255, 255, 255)
DARK = (24, 28, 36)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, spacing=6):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.text((48, 26), "THE WORLD IN ONE DAY", font=font(SERIF, 58), fill=INK)
d.line([(48, 108), (976, 108)], fill=INK, width=4)
d.line([(48, 114), (976, 114)], fill=INK, width=1)
d.text((48, 128), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 26), fill=RED)
d.text((976, 128), "make.fun", font=font(SANS, 24), fill=GREY, anchor="ra")

# ---- lead story: NATO / Poland ----
ly = 178
d.rectangle([48, ly, 976, ly + 268], fill=CARD, outline=LINE, width=2)
d.text((72, ly + 16), "NATO  •  POLAND", font=font(SANS_B, 22), fill=RED)
y = draw_wrapped(
    d, 72, ly + 48,
    "NATO sends AWACS to Poland as a Russian drone slips across its border",
    font(SERIF, 40), 880, spacing=4)
d.line([(72, y + 8), (952, y + 8)], fill=LINE, width=1)
draw_wrapped(
    d, 72, y + 22,
    "Allies agreed the early-warning deployment in Brussels after three "
    "Russian missiles landed in Poland on Friday. Overnight, Warsaw put its "
    "air defences on alert as a Russian drone briefly crossed the border "
    "during a fresh strike on Ukraine.",
    font(SANS, 22), 880, spacing=5)

# ---- second row: two half-width stories ----
ry = 458
for x0, kicker, head, body in [
    (48, "KOREA", "Jets scrambled over Russian warplanes",
     "South Korea scrambled jets after Russian warplanes entered its air "
     "defence zone; a suspected North Korean aircraft also breached airspace "
     "near Ulleung island."),
    (528, "LIBYA  •  UKRAINE", "Kyiv sinks a Russian warship far from home",
     "Ukraine says sea drones sank a Russian warship off Libya, destroying "
     "a Ka-27 helicopter and hitting the cargo ship MV Angara — the war's "
     "reach spreading beyond Europe."),
]:
    d.rectangle([x0, ry, x0 + 448, ry + 240], fill=CARD, outline=LINE, width=2)
    d.text((x0 + 20, ry + 14), kicker, font=font(SANS_B, 20), fill=RED)
    yy = draw_wrapped(d, x0 + 20, ry + 44, head, font(SERIF, 27), 408, spacing=3)
    draw_wrapped(d, x0 + 20, yy + 6, body, font(SANS, 19), 408, spacing=4)

# ---- grid: four cards ----
gy = 706
cards = [
    ("TECH", "Nvidia brings back Jensen Huang",
     "The board reinstated Huang 11 days after he quit, following pressure "
     "from Trump."),
    ("USA", "Democrats take their biggest House majority in decades",
     "The victory hands Democrats power to block Trump's agenda and probe "
     "alleged corruption."),
    ("ZANZIBAR", "Fire engulfs six hotels; 180 tourists evacuated",
     "A blaze swept six hotels on Tanzania's Zanzibar island; guests were "
     "moved to safety."),
    ("USA", "Honda recalls 810,000 cars over airbag risk",
     "Takata inflators could rupture and spray metal fragments, the carmaker "
     "warned."),
]
for i, (kicker, head, body) in enumerate(cards):
    x0 = 48 + (i % 2) * 480
    y0 = gy + (i // 2) * 128
    d.rectangle([x0, y0, x0 + 448, y0 + 120], fill=CARD, outline=LINE, width=1)
    d.text((x0 + 16, y0 + 10), kicker, font=font(SANS_B, 17), fill=RED)
    yy = draw_wrapped(d, x0 + 16, y0 + 34, head, font(SERIF, 21), 416, spacing=2)
    draw_wrapped(d, x0 + 16, yy + 2, body, font(SANS, 16), 416, spacing=3)

# ---- bottom ticker ----
ty = 962
d.rectangle([0, ty, W, H], fill=DARK)
ticker = ("PAKISTAN QUAKE 4.1  •  DENMARK TO BAN SCHOOL PHONES  •  "
          "N. KOREA THREATENS SWISS OFFICE  •  2031 WORLD CUP: USA, MEXICO, "
          "COSTA RICA, JAMAICA  •  RUSSIAN WAR DEAD NEAR 500,000")
lines = wrap(d, ticker, font(SANS_B, 16), 928)
yy = ty + 10
for ln in lines:
    d.text((48, yy), ln, font=font(SANS_B, 16), fill=(235, 230, 220))
    yy += 22

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
