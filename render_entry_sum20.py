#!/usr/bin/env python3
"""Render ENTRY sum20 (news-image-20261120) — 50 cerita, DENGAN ILUSTRASI.
Dibangun dari sketch_grid_sum20.py (sketsa grid yang sudah disetujui user):
layout + data + teks SAMA PERSIS, kotak placeholder diganti paste ilustrasi
PNG yang sudah disetujui user (16 file, 1x, ukuran pas: hero 190x102,
strip 159x48, paste langsung tanpa resize).
Flag ENABLE_HEROES / ENABLE_STRIPS mengontrol paste per jenis (M1: keduanya
False = output identik sketsa, untuk diff; M2: hero True; M4: strip True).
Output: entry-20nov.png (1024x1024). Versi 300px ditambahkan di revisi
setelah M3 (bukan di M1).
"""
from PIL import Image, ImageDraw, ImageFont
import os
import sys
sys.path.insert(0, "/home/hatch/workspace/makefun/news-image/50story")
from grid_sketch_v4_17nov import CONTINENTS, GULF_WATER

OUT = os.path.expanduser("~/workspace/makefun/news-image/50story/entry-20nov.png")
OUT300 = os.path.expanduser("~/workspace/makefun/news-image/50story/entry-20nov-300px.png")
FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except Exception:
        return ImageFont.load_default()

PAPER = (250, 246, 236)
INK = (22, 34, 46)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
TINT2 = (244, 238, 226)
GREY = (120, 120, 120)
GREEN = (34, 139, 34)
BLUE = (30, 90, 168)
AMBER = (217, 164, 32)
PURPLE = (120, 60, 140)
ORANGE = (230, 120, 30)
TEAL = (0, 150, 150)
OCEAN = (208, 224, 240)
LAND = (233, 229, 218)
LAND_OUTLINE = (190, 185, 170)
GRAT = (190, 200, 205)
LEADER = (140, 140, 140)
RED_DK = (138, 43, 27)
PLACE_BG = (232, 230, 224)
PLACE_LINE = (150, 150, 150)
PLACE_TXT = (110, 110, 110)

def placeholder(d, box, label, sub=""):
    """Kotak kosong berlabel untuk area ilustrasi (tanpa gambar)."""
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=PLACE_BG)
    for x in range(x0, x1, 8):
        d.line([(x, y0), (min(x + 5, x1), y0)], fill=PLACE_LINE, width=1)
        d.line([(x, y1), (min(x + 5, x1), y1)], fill=PLACE_LINE, width=1)
    for y in range(y0, y1, 8):
        d.line([(x0, y), (x0, min(y + 5, y1))], fill=PLACE_LINE, width=1)
        d.line([(x1, y), (x1, min(y + 5, y1))], fill=PLACE_LINE, width=1)
    f = F("DejaVuSans-Bold.ttf", 9)
    tw = d.textlength(label, font=f)
    cy = (y0 + y1) // 2
    if sub:
        d.text(((x0 + x1 - tw) / 2, cy - 10), label, font=f, fill=PLACE_TXT)
        f2 = F("DejaVuSans.ttf", 8)
        tw2 = d.textlength(sub, font=f2)
        d.text(((x0 + x1 - tw2) / 2, cy + 4), sub, font=f2, fill=(140, 140, 140))
    else:
        d.text(((x0 + x1 - tw) / 2, cy - 5), label, font=f, fill=PLACE_TXT)

# ---- ilustrasi: paste file PNG yang sudah disetujui (ukuran pas, tanpa resize) ----
ILLU_DIR = os.path.expanduser("~/workspace/makefun/news-image/50story/illustrations/")
ENABLE_HEROES = True  # M1: False (diff vs sketsa); M2: True
ENABLE_STRIPS = True  # M1/M2: False; M4: True
HERO_FILES = {1: "sum20-h1-meltdown.png", 2: "sum20-h2-gtavi.png",
              3: "sum20-h3-ukraine.png", 4: "sum20-h4-summit.png"}
STRIP_FILES = {5: "sum20-a1-anthropic.png", 6: "sum20-a2-icj.png",
               7: "sum20-a3-cop31.png", 8: "sum20-a4-huang.png",
               9: "sum20-a5-microsoft.png", 10: "sum20-a6-eu-cyber.png",
               11: "sum20-a7-suncatcher.png", 12: "sum20-a8-muse.png",
               13: "sum20-a9-blackhole.png", 14: "sum20-a10-cyclone.png",
               15: "sum20-a11-hormuz.png", 16: "sum20-a12-rosalia.png"}

def paste_hero(d, box, num, label, sub=""):
    """Paste hero 190x102 ke box (x0+6, y0+6, x0+196, y1-6); kalau
    ENABLE_HEROES False, gambar kotak placeholder seperti sketsa."""
    if not ENABLE_HEROES:
        placeholder(d, box, label, sub)
        return
    x0, y0, x1, y1 = box
    illu = Image.open(os.path.join(ILLU_DIR, HERO_FILES[num])).convert("RGB")
    assert illu.size == (x1 - x0, y1 - y0), f"hero #{num} size {illu.size} != box {(x1 - x0, y1 - y0)}"
    im.paste(illu, (x0, y0))

def paste_strip(d, box, num, label, sub=""):
    """Paste strip 159x48 ke box (x0, y0, x1, y0+48); kalau
    ENABLE_STRIPS False, gambar kotak placeholder seperti sketsa."""
    if not ENABLE_STRIPS:
        placeholder(d, box, label, sub)
        return
    x0, y0, x1, y1 = box
    illu = Image.open(os.path.join(ILLU_DIR, STRIP_FILES[num])).convert("RGB")
    assert illu.size == (x1 - x0, y1 - y0), f"strip #{num} size {illu.size} != box {(x1 - x0, y1 - y0)}"
    im.paste(illu, (x0, y0))

# --- fungsi peta asli (dari sketch_grid_round2_4hero_full.py) ---
LAT_TOP, LAT_BOT = 90.0, -90.0
LON0, LON1 = -130.0, 150.0
LON_SPAN = LON1 - LON0

def project(lon, lat, x0, y0, w, h):
    span = LAT_TOP - LAT_BOT
    return (x0 + (lon - LON0) / LON_SPAN * w,
            y0 + (LAT_TOP - lat) / span * h)

def draw_pin(d, x, y, num, color, r=7):
    f = F("DejaVuSans-Bold.ttf", 9 if num < 10 else 8)
    d.ellipse([x - r, y - r, x + r, y + r], fill=color,
              outline=(255, 255, 255), width=1)
    d.text((x, y), str(num), font=f, fill=(255, 255, 255), anchor="mm")

def seg_cross(p1, p2, p3, p4):
    def _d(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = _d(p3, p4, p1), _d(p3, p4, p2)
    d3, d4 = _d(p1, p2, p3), _d(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))

def place_pins(draw, spots, colors, r=7, x0=0, y0=0, x1=None, y1=None, avoid=None):
    placed, displaced, leaders = [], [], []
    steps = [0, 9, -9, 18, -18, 26, -26, 36, -36, 44, -44]
    cands = [(dx, dy) for dx in steps for dy in steps]
    cands.sort(key=lambda p: (p[0] ** 2 + p[1] ** 2, abs(p[1]), abs(p[0])))
    for (num, x, y), color in zip(spots, colors):
        min_d = 2 * r + 2
        bases = [(x, y)]
        if avoid is not None:
            ax0, ay0, ax1, ay1 = avoid
            if (ax0 - r - 1 < x < ax1 + r + 1
                    and ay0 - r - 1 < y < ay1 + r + 1):
                esc = [(x, ay0 - r - 1), (x, ay1 + r + 1),
                       (ax0 - r - 1, y), (ax1 + r + 1, y)]
                esc.sort(key=lambda p: (p[0] - x) ** 2 + (p[1] - y) ** 2)
                bases = esc + [(x, y)]
        done = False
        for bx, by in bases:
            for ox, oy in cands:
                cx, cy = bx + ox, by + oy
                if x1 is not None:
                    cx = min(max(cx, x0 + r + 1), x1 - r - 1)
                    cy = min(max(cy, y0 + r + 1), y1 - r - 1)
                if avoid is not None:
                    ax0, ay0, ax1, ay1 = avoid
                    if (ax0 - r - 1 < cx < ax1 + r + 1
                            and ay0 - r - 1 < cy < ay1 + r + 1):
                        continue
                if not all((cx - px) ** 2 + (cy - py) ** 2 >= min_d ** 2
                           for px, py in placed):
                    continue
                if abs(cx - x) > 1 or abs(cy - y) > 1:
                    if any(seg_cross((cx, cy), (x, y), s[0], s[1])
                           for s in leaders):
                        continue
                placed.append((cx, cy))
                if abs(cx - x) > 1 or abs(cy - y) > 1:
                    displaced.append((num, round(x), round(y),
                                      round(cx), round(cy)))
                    leaders.append(((cx, cy), (x, y)))
                draw_pin(draw, cx, cy, num, color, r=r)
                done = True
                break
            if done:
                break
        if not done:
            fx = min(max(x, x0 + r + 1), x1 - r - 1) if x1 is not None else x
            fy = min(max(y, y0 + r + 1), y1 - r - 1) if y1 is not None else y
            placed.append((fx, fy))
            draw_pin(draw, fx, fy, num, color, r=r)
    return placed, displaced, leaders

# ---------- data sum20 (tesis §3) ----------
# Hero: (nomor, warna region, tag, chip, warna chip, headline 2 baris,
#        dek 2 baris, label placeholder, sub placeholder)
HEROES = [
    (1, GREEN, "AMERICAS", "CONFIRMED · INVESTOPEDIA", GREEN,
     ("AI MELTDOWN:", "NASDAQ −5.2%"),
     ("Nasdaq falls 5.2%, worst week since April 2025;",
      "Nvidia −14% after Huang resigns. Reuters"),
     "HERO ILLUSTRATION", "AI MELTDOWN — STOCK CHART"),
    (2, GREEN, "AMERICAS · MIAMI", "CONFIRMED · BARRON'S", GREEN,
     ("GTA VI: $3.79B", "DAY ONE"),
     ("GTA VI sells $3.79bn on day one, the biggest",
      "entertainment launch ever; 32.5m copies. Barron's"),
     "HERO ILLUSTRATION", "GTA VI — VICE CITY NEON"),
    (3, BLUE, "EUROPE · KYIV", "CONFIRMED · REUTERS", GREEN,
     ("RUSSIA HITS", "UKRAINE, POLAND"),
     ("Russia fires 400+ drones and 110 missiles;",
      "two fall in Poland (NATO); 30 die in Kramatorsk."),
     "HERO ILLUSTRATION", "MISSILES — KYIV, MAP"),
    (4, RED, "ASIA · SHENZHEN", "CONFIRMED · REUTERS", GREEN,
     ("TRUMP–XI–PUTIN:", "NO NUKES"),
     ("Trump, Xi, Putin meet in Shenzhen; agree",
      "'nuclear war must never happen.' Reuters"),
     "HERO ILLUSTRATION", "SUMMIT — THREE LEADERS"),
]

# Tier A: (nomor, warna region, tag, chip, warna chip,
#          headline 2 baris, fakta 2 baris, label strip, sub strip)
TIER = [
    (5, GREEN, "AMERICAS · NEW YORK", "CONFIRMED · INVESTOPEDIA", GREEN,
     ("ANTHROPIC FALLS", "9% DAY AFTER IPO"),
     ("Anthropic falls 9% a day", "after its $81.3bn IPO."),
     "STRIP #5", "IPO BELL + STOCK CHART"),
    (6, BLUE, "EUROPE · THE HAGUE", "CONFIRMED · CNN", GREEN,
     ("MYANMAR REJECTS", "ICJ RULING"),
     ("Myanmar rejects the", "first genocide ruling."),
     "STRIP #6", "ICJ BUILDING + GAVEL"),
    (7, BLUE, "EUROPE · ANTALYA", "OFFICIAL · DRAFT", BLUE,
     ("COP31 SPLITS OVER", "FOSSIL FUELS"),
     ("Fossil-fuel language", "unsettled; AMOC risk 50%."),
     "STRIP #7", "MELTING GLACIER"),
    (8, GREEN, "SANTA CLARA", "CONFIRMED · GADGETS 360", GREEN,
     ("NVIDIA CEO HUANG", "RESIGNS AT ONCE"),
     ("Jensen Huang resigns", "with immediate effect."),
     "STRIP #8", "GPU CHIP"),
    (9, GREEN, "AMERICAS · REDMOND", "REPORTED · 1 OUTLET", AMBER,
     ("MICROSOFT 365", "DOWN WORLDWIDE"),
     ("Microsoft 365 down", "globally for 9+ hours."),
     "STRIP #9", "ERROR SCREEN"),
    (10, BLUE, "EUROPE · BRUSSELS", "REPORTED · NEURON", AMBER,
     ("EU COMMISSION HIT", "BY CYBERATTACK"),
     ("AI-assisted attack hits", "pay and medical systems."),
     "STRIP #10", "CYBER SHIELD"),
    (11, GREEN, "CAPE CANAVERAL", "REPORTED · NEURON", AMBER,
     ("GOOGLE SENDS AI", "SERVERS TO ORBIT"),
     ("Suncatcher sends AI", "to orbit; Blue Origin."),
     "STRIP #11", "SATELLITE + EARTH"),
    (12, GREEN, "MENLO PARK", "CONFIRMED · REUTERS", GREEN,
     ("META'S MUSE LEAKS", "PRIVATE CHATS"),
     ("Meta AI agent Muse", "leaks private chats."),
     "STRIP #12", "PHONE + CHAT + LOCK"),
    (13, GREEN, "AMERICAS · BERKELEY", "OFFICIAL · SCIENCE", BLUE,
     ("CLAUDE CRACKS", "BLACK HOLES"),
     ("Claude solves graduate", "black-hole physics."),
     "STRIP #13", "BLACK HOLE + RING"),
    (14, TEAL, "OCEANIA · PACIFIC", "OFFICIAL · NATURE", BLUE,
     ("CYCLONES PEAK", "FASTER, STUDY SAYS"),
     ("Tropical cyclones reach", "peak intensity faster."),
     "STRIP #14", "CYCLONE FROM SPACE"),
    (15, PURPLE, "MID EAST · HORMUZ", "REPORTED · APPISTOS", AMBER,
     ("TANKER BURNS", "IN HORMUZ STRAIT"),
     ("Tanker burns after", "attack in Hormuz Strait."),
     "STRIP #15", "BURNING TANKER"),
    (16, BLUE, "EUROPE · MADRID", "CONFIRMED · BRIEF NEWS", GREEN,
     ("ROSALÍA'S 'LUX':", "3 LATIN GRAMMYS"),
     ("Rosalía wins 3 Latin", "Grammys; 9 noms."),
     "STRIP #16", "MIC + GRAMMY TROPHY"),
]

# Brief 34 — urut region: AS 9, EU 12, ME 1, AM 11, OC 1 (tesis §3.3)
BRIEFS = [
    # AS (9) — #17-25
    "Tu-95 — Taiwan ADIZ", "APEC — Shenzhen Outlook", "India — Energy growth",
    "Tencent — Hy4 open", "US sanctions — Cambodia", "China bonds — $2B",
    "Pakistan — Bus crash", "Korea — Exam scandal", "BTS — 10B streams",
    # EU (12) — #26-37
    "Kyiv — Dutch embassy hit", "Frankfurt — Bomb plot", "UK — Joanne Young case",
    "BepiColombo — X-ray first", "Hera — DART crater map", "EU-UK — Summit Brussels",
    "Denmark — Arctic deal", "ECB — Two candidates", "EU — €1B Ukraine aid",
    "Estonia — Border closed", "Spain — Feijóo wins debate",
    # ME (1) — #37
    "Trump — Iran strike delayed",
    # AM (11) — #38-48
    "US cyber chief — Resigns", "California — Nvidia probe", "Visa/MC/JPM — Vendor hack",
    "Intuit — Mailchimp $3.68B", "GLP-1 — Weight training", "Thinking Machines — Inkling",
    "Haiti — 34 gang members", "Argentina — Disability law", "US consumer — Sentiment",
    "Ella Langley — 6 CMA wins", "Harry Styles — MSG finale",
    # AF (1) — #49 (SWAP 21 Nov: ganti B33 Pattinson, biar Afrika ada)
    "Mlambo-Ngcuka dies at 71",
    # OC (1) — #50
    "Tame Impala — 7 ARIAs",
]
BRIEF_NUM = list(range(17, 51))
BRIEF_REGION = (
    [RED] * 9 + [BLUE] * 11 + [PURPLE] * 1 + [GREEN] * 11 + [ORANGE] * 1 + [TEAL] * 1
)
assert len(BRIEFS) == 34 and len(BRIEF_NUM) == 34 and len(BRIEF_REGION) == 34

TIMELINE = [
    ("Overnight", "Shenzhen summit opens"),
    ("Morning", "Myanmar rejects ICJ ruling"),
    ("Midday", "GTA VI sales announced"),
    ("Afternoon", "Anthropic shares fall 9%"),
    ("Evening", "Missiles fall in Poland"),
    ("Night", "Nasdaq worst week"),
]

# pin: (nomor, lat, lon) — 50 cerita, tiap nomor #1-50 tepat sekali.
PINS50 = [
    (1, 40.7, -74.0), (2, 25.8, -80.2), (3, 50.4, 30.5), (4, 22.5, 114.0),
    (5, 37.8, -122.4), (6, 52.1, 4.3), (7, 36.9, 30.7), (8, 37.4, -121.9),
    (9, 47.6, -122.1), (10, 50.8, 4.4), (11, 28.4, -80.6), (12, 37.5, -122.2),
    (13, 37.9, -122.3), (14, 15.0, 135.0), (15, 26.5, 56.0), (16, 40.4, -3.7),
    (17, 23.7, 121.0), (18, 22.5, 114.0), (19, 28.6, 77.2), (20, 22.5, 114.0),
    (21, 11.5, 104.9), (22, 39.9, 116.4), (23, 31.5, 74.3), (24, 37.6, 127.0),
    (25, 35.7, 139.7), (26, 50.4, 30.5), (27, 50.1, 8.7), (28, 51.5, -0.1),
    (29, 49.9, 8.7), (30, 49.9, 8.7), (31, 50.8, 4.4), (32, 55.7, 12.6),
    (33, 50.1, 8.7), (34, 50.8, 4.4), (35, 59.4, 24.7), (36, 40.4, -3.7),
    (37, 35.7, 51.4), (38, 38.9, -77.0), (39, 38.6, -121.5), (40, 40.7, -74.0),
    (41, 37.4, -122.1), (42, 40.7, -74.0), (43, 37.8, -122.4), (44, 18.5, -72.3),
    (45, -34.6, -58.4), (46, 40.7, -74.0), (47, 36.2, -86.8), (48, 40.7, -74.0),
    (49, -26.2, 28.0), (50, -33.9, 151.2),
]
assert sorted(n for n, _, _ in PINS50) == list(range(1, 51)), "PINS50 harus #1-50"

REGION50 = {
    1: "AM", 2: "AM", 3: "EU", 4: "AS", 5: "AM", 6: "EU", 7: "EU", 8: "AM",
    9: "AM", 10: "EU", 11: "AM", 12: "AM", 13: "AM", 14: "OC", 15: "ME",
    16: "EU",
}
for n in range(17, 26):
    REGION50[n] = "AS"
for n in range(26, 37):
    REGION50[n] = "EU"
REGION50[37] = "ME"
for n in range(38, 49):
    REGION50[n] = "AM"
REGION50[49] = "AF"
REGION50[50] = "OC"
REG_COL = {"AS": RED, "AM": GREEN, "EU": BLUE, "ME": PURPLE, "AF": ORANGE, "OC": TEAL}

W, H = 1024, 1024
im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

f_title = F("DejaVuSerif-Bold.ttf", 40)
f_hero = F("DejaVuSerif-Bold.ttf", 16)
f_head = F("DejaVuSerif-Bold.ttf", 12)
f_tag = F("DejaVuSans-Bold.ttf", 10)
f_fact = F("DejaVuSans.ttf", 11)
f_small = F("DejaVuSans.ttf", 11)
f_small_b = F("DejaVuSans-Bold.ttf", 11)
f_tiny = F("DejaVuSans.ttf", 10)
f_chip = F("DejaVuSans-Bold.ttf", 9)
f_idx = F("DejaVuSans.ttf", 12)
f_kick = F("DejaVuSans-Bold.ttf", 10)
f_badge = F("DejaVuSans-Bold.ttf", 8)

def chip_text(c, col):
    return WHITE if col != AMBER else INK

y = 10
# ---- Masthead 62px ----
d.rectangle([14, y, 1010, y + 62], fill=WHITE)
d.rectangle([14, y + 60, 1010, y + 62], fill=RED)
d.text((24, y + 2), "THE WORLD IN ONE PAGE", font=f_kick, fill=RED)
d.text((24, y + 14), "Friday 20 November 2026", font=f_title, fill=INK)
d.text((1010, y + 2), "50 STORIES · 6 REGIONS · EVERY ONE FROM THIS FRIDAY",
       font=f_kick, fill=INK, anchor="ra")
y += 62 + 4

# ---- Timeline 40px ----
d.rectangle([14, y, 1010, y + 40], fill=TINT2)
d.rectangle([14, y, 114, y + 40], fill=RED)
d.text((64, y + 10), "THE DAY", font=F("DejaVuSans-Bold.ttf", 11), fill=WHITE, anchor="mm")
d.text((64, y + 26), "IN UTC", font=F("DejaVuSans-Bold.ttf", 11), fill=WHITE, anchor="mm")
tx = 124
for (t, txt) in TIMELINE:
    d.text((tx, y + 4), t, font=F("DejaVuSans-Bold.ttf", 11), fill=RED)
    d.text((tx, y + 20), txt, font=f_tiny, fill=INK)
    tx += 148
for dx in (272, 420, 568, 716, 864):
    d.line([(dx, y + 4), (dx, y + 36)], fill=(200, 200, 200), width=1)
d.line([(14, y + 40), (1010, y + 40)], fill=INK, width=2)
y += 40 + 4

# ---- Heroes 2 baris x 2 kolom, 114px (kotak ilustrasi KOSONG) ----
def hero(x0, x1, y0, y1, num, reg_c, tag, chip, chip_c, heads, deks, lab, sub):
    t1, t2 = heads
    dek1, dek2 = deks
    d.rectangle([x0, y0, x1, y1], fill=WHITE)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    paste_hero(d, (x0 + 6, y0 + 6, x0 + 196, y1 - 6), num, lab, sub)
    tx = x0 + 202
    d.ellipse([tx, y0 + 5, tx + 12, y0 + 17], fill=reg_c)
    d.text((tx + 6, y0 + 11), str(num), font=F("DejaVuSans-Bold.ttf", 7), fill=WHITE, anchor="mm")
    d.text((tx + 15, y0 + 5), tag, font=f_tag, fill=reg_c)
    cw = d.textlength(chip, font=f_chip) + 8
    d.rectangle([x1 - 6 - cw, y0 + 5, x1 - 6, y0 + 18], fill=chip_c)
    d.text((x1 - 6 - cw // 2, y0 + 11), chip, font=f_chip, fill=chip_text(chip, chip_c), anchor="mm")
    d.text((tx, y0 + 24), t1, font=f_hero, fill=INK)
    d.text((tx, y0 + 46), t2, font=f_hero, fill=INK)
    d.text((tx, y0 + 72), dek1, font=f_small, fill=INK)
    d.text((tx, y0 + 87), dek2, font=f_small, fill=INK)

hero(14, 506, y, y + 114, *HEROES[0])
hero(518, 1010, y, y + 114, *HEROES[1])
y += 114 + 6
hero(14, 506, y, y + 114, *HEROES[2])
hero(518, 1010, y, y + 114, *HEROES[3])
y += 114 + 10

# ---- Grid Tier A 2x6, sel 159x139, strip 159x48 KOSONG ----
CELL_H = 139
XS = [14, 181, 348, 515, 682, 849]
YS = [y, y + CELL_H + 8]
for r in range(2):
    for c in range(6):
        n = r * 6 + c
        num, reg_c, tag, chip, chip_c, (h1, h2), (f1, f2), lab, sub = TIER[n]
        x0, y0 = XS[c], YS[r]
        x1, y1 = x0 + 159, y0 + CELL_H
        d.rectangle([x0, y0, x1, y1], fill=WHITE if (r + c) % 2 == 0 else TINT2)
        paste_strip(d, (x0, y0, x1, y0 + 48), num, lab, sub)
        d.ellipse([x0 + 4, y0 + 51, x0 + 17, y0 + 64], fill=reg_c)
        d.text((x0 + 10.5, y0 + 57.5), str(num), font=f_badge, fill=WHITE, anchor="mm")
        d.text((x0 + 20, y0 + 51), tag, font=f_tag, fill=reg_c)
        cw = d.textlength(chip, font=f_chip) + 8
        d.rectangle([x0 + 4, y0 + 66, x0 + 4 + cw, y0 + 79], fill=chip_c)
        d.text((x0 + 4 + cw // 2, y0 + 72.5), chip, font=f_chip, fill=chip_text(chip, chip_c), anchor="mm")
        d.text((x0 + 4, y0 + 82), h1, font=f_head, fill=INK)
        d.text((x0 + 4, y0 + 97), h2, font=f_head, fill=INK)
        d.text((x0 + 4, y0 + 113), f1, font=f_fact, fill=(60, 60, 60))
        d.text((x0 + 4, y0 + 126), f2, font=f_fact, fill=(60, 60, 60))
y = YS[1] + CELL_H + 8

d.line([(14, y - 4), (1010, y - 4)], fill=INK, width=1)

# ---- Zone head 16px ----
d.text((14, y), "WHERE IT HAPPENED", font=F("DejaVuSans-Bold.ttf", 13), fill=RED)
d.text((326, y), "ALSO ON FRIDAY 20 NOVEMBER", font=F("DejaVuSans-Bold.ttf", 13), fill=RED)
y += 16 + 2

# ---- Zona brief 280px: peta asli + indeks 34 (12/11/11), brief 12pt, baris 23px ----
BZ0 = y
BRIEF_H = 280
d.rectangle([14, BZ0, 314, BZ0 + BRIEF_H], fill=(216, 232, 220))
d.text((24, BZ0 + 8), "WORLD MAP — 50 STORIES", font=F("DejaVuSans-Bold.ttf", 13), fill=INK)
MAP_W = 280
ATLAS_H = int(round(180 * MAP_W / 280))  # 180
ax = 14 + (300 - MAP_W) // 2
ay = BZ0 + 26
atlas = Image.new("RGB", (MAP_W, ATLAS_H), OCEAN)
md = ImageDraw.Draw(atlas)
for lat in (-60, -30, 0, 30, 60):
    _, gyy = project(0, lat, 0, 0, MAP_W, ATLAS_H)
    md.line([(0, gyy), (MAP_W, gyy)], fill=GRAT, width=1)
for lon in (-120, -60, 0, 60, 120):
    gx, _ = project(lon, 0, 0, 0, MAP_W, ATLAS_H)
    md.line([(gx, 0), (gx, ATLAS_H)], fill=GRAT, width=1)
for _, poly in CONTINENTS:
    pts = [project(lon, lat, 0, 0, MAP_W, ATLAS_H) for lon, lat in poly]
    md.polygon(pts, fill=LAND, outline=LAND_OUTLINE)
iw, ih = 80, 45
ix0, iy0 = 8, ATLAS_H - ih - 8
IN_LON0, IN_LON1, IN_LAT0, IN_LAT1 = 46.0, 58.0, 23.0, 31.0
inset_pins = [(n, la, lo) for n, la, lo in PINS50
              if IN_LON0 <= lo <= IN_LON1 and IN_LAT0 <= la <= IN_LAT1]
inset_keys = {(n, la, lo) for n, la, lo in inset_pins}
main_pos, main_col = [], []
for num, lat, lon in PINS50:
    if (num, lat, lon) in inset_keys:
        continue
    px, py = project(lon, lat, 0, 0, MAP_W, ATLAS_H)
    main_pos.append((num, px, py))
    main_col.append(REG_COL[REGION50[num]])
placed, displaced, leaders = place_pins(
    md, main_pos, main_col, r=7, x0=0, y0=0, x1=MAP_W, y1=ATLAS_H,
    avoid=(ix0, iy0, ix0 + iw, iy0 + ih))
for (px_, py_), (tx_, ty_) in leaders:
    md.line([(px_, py_), (tx_, ty_)], fill=LEADER, width=1)
def in_proj(lon, lat):
    return (ix0 + (lon - IN_LON0) / (IN_LON1 - IN_LON0) * iw,
            iy0 + (IN_LAT1 - lat) / (IN_LAT1 - IN_LAT0) * ih)
gpts = [in_proj(lon, lat) for lon, lat in GULF_WATER]
md.rectangle([ix0, iy0, ix0 + iw, iy0 + ih], fill=LAND, outline=INK, width=1)
md.polygon(gpts, fill=OCEAN, outline=LAND_OUTLINE)
md.text((ix0 + 5, iy0 + 3), "THE GULF", font=F("DejaVuSans-Bold.ttf", 8), fill=INK)
for num, lat, lon in inset_pins:
    px_, py_ = in_proj(lon, lat)
    draw_pin(md, px_, py_, num, REG_COL[REGION50[num]], r=4)
im.paste(atlas, (ax, ay))
d.rectangle([ax, ay, ax + MAP_W - 1, ay + ATLAS_H - 1], outline=INK, width=1)
# legenda region — 1 baris 10pt (sum20: 9 -> 10pt)
ly = ay + ATLAS_H + 2
lx = 14
f_leg = F("DejaVuSans.ttf", 10)
for code, lab in [("EU", "Europe"), ("ME", "Mid East"), ("AS", "Asia"),
                  ("AM", "Americas"), ("AF", "Africa"), ("OC", "Oceania")]:
    d.ellipse([lx, ly + 2, lx + 8, ly + 10], fill=REG_COL[code])
    d.text((lx + 11, ly), lab, font=f_leg, fill=INK)
    lx += 11 + d.textlength(lab, font=f_leg) + 3
assert lx - 5 <= 314, f"legenda 1 baris meluber: {lx - 5 - 14}px > 300"
d.text((24, ly + 15), "50 of 50 pinned · lat -90° to +90°", font=f_tiny, fill=INK)
# indeks 34 brief — nomor di lingkaran warna region, teks INK 12pt, baris 23px
for i, x0 in enumerate([326, 548, 770]):
    rows = [12, 11, 11][i]
    for j in range(rows):
        idx = sum([12, 11, 11][:i]) + j
        if idx >= len(BRIEFS):
            break
        yy = BZ0 + j * 23
        d.rectangle([x0, yy, x0 + 200, yy + 21], fill=WHITE if j % 2 == 0 else TINT2)
        rc = BRIEF_REGION[idx]
        d.ellipse([x0 + 3, yy + 3, x0 + 17, yy + 17], fill=rc)
        d.text((x0 + 10, yy + 10), str(BRIEF_NUM[idx]), font=F("DejaVuSans-Bold.ttf", 7), fill=WHITE, anchor="mm")
        d.text((x0 + 21, yy + 5), BRIEFS[idx], font=f_idx, fill=INK)
y = BZ0 + BRIEF_H + 2

# ---- Date-check 28px ----
d.rectangle([14, y, 1010, y + 28], outline=RED_DK, width=1)
d.rectangle([14, y, 106, y + 28], fill=RED)
d.text((60, y + 14), "DATE CHECK", font=f_small_b, fill=WHITE, anchor="mm")
d.text((114, y + 4), "ICJ ruled 19 Nov — 20 Nov is Myanmar REJECTING it. Anthropic IPO priced 18 Nov, trading 19 Nov — 20 Nov is shares FALLING 9%.", font=f_tiny, fill=INK)
d.text((114, y + 17), "GTA VI released 19 Nov — 20 Nov is the $3.79bn sales ANNOUNCEMENT. Not yet: trilateral declaration text, COP31 final text.", font=f_tiny, fill=INK)
y += 28 + 3

# ---- Footer 26px ----
d.line([(14, y - 2), (1010, y - 2)], fill=RED, width=1)
d.text((14, y), "Every story here happened or was first reported on Friday 20 November 2026. CLAIM = one side's account, not independently confirmed.", font=f_tiny, fill=GREY)
d.text((14, y + 12), "Sources: Reuters, Investopedia, CNN, BBC, Nature, Barron's, Amnesty, The Neuron. Original drawings.", font=f_tiny, fill=GREY)
y += 26 + 7

im.save(OUT)
im.resize((300, 300), Image.LANCZOS).save(OUT300)
print("saved", OUT, im.size, "pins:", len(PINS50), "briefs:", len(BRIEFS),
      "TOTAL =", y, "/ 1024, slack =", 1024 - y)
print("300px:", OUT300)
