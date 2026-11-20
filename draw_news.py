#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one front page summing up Friday
20 November 2026, drawn with Pillow at build time (the entry itself is the
finished entry.png, copied by main.ts).

Layout (1024x1024): masthead naming the day, a Shenzhen lead beside a
The Hague box, three feature boxes (Kyiv, Anthropic's debut, Washington),
three columns of short items, a markets strip with Thursday's closes and
a sources footer. About 22 distinct stories, every one reported on
20 November 2026.

Facts used (all reported 20 Nov 2026; sources AP, Reuters, BBC, Le Monde):
  Shenzhen: Trump, Putin and Xi hold first-ever trilateral talks at APEC
    in Shenzhen and release a 'peace declaration'; sources call it vague,
    with no significant agreements on Ukraine or nuclear arms.
  The Hague: the International Court of Justice finds Myanmar committed
    genocide against the Rohingya, 9-6, the first such ruling in the
    court's 80-year history; Rohingya in Bangladesh welcome it and say
    they want to go home.
  Kyiv: Russian missiles and drones hit Kyiv overnight; 3 killed, 9
    injured; several bridges damaged and power cut. The EU will summon
    Russia's envoy over damage to its embassy in the strikes.
  London: the UK pledges more than 1,000 drones for Ukraine in a
    260-million-pound package.
  Washington: the Senate rejects an Iran war-powers resolution, 51-48;
    the Pentagon puts the Iran war's cost at $48.3 billion; Trump
    posthumously pardons baseball legend Pete Rose.
  Markets: Anthropic soars on its Nasdaq debut, the first purely AI
    company to list, valuing it near $2 trillion. Thursday's closes:
    S&P 500 7,175.83 -2.02% (sixth straight loss), Dow 49,097.06 -2.19%
    (first close below 50,000 since June), Nasdaq 23,879.20 -2.25%,
    VIX 28.44, gold $3,685.50 -1.51%, Brent $91.98 +0.03%, Bitcoin
    about $62,150 on Friday morning.
  Shorts: Poland investigates unknown objects as an air-threat warning
    is lifted; Genoa airport suspends flights after unidentified drones;
    Houthis claim strikes on four Saudi targets and Saudi defences down
    two drones; a tanker catches fire after hitting a mine east of the
    Strait of Hormuz; a 5.6-magnitude quake strikes near New Caledonia;
    a gas explosion in Georgia kills six; a fire in a French apartment
    block kills one and injures 15; an Israeli strike hits a Hezbollah
    site in eastern Lebanon; the UK and EU agree a youth mobility
    scheme; Kamala Harris meets Emmanuel Macron in Paris; Las Vegas
    Grand Prix practice is washed out; Fiona the hippo dies at
    Cincinnati Zoo after swallowing a hat.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (29, 78, 137)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading=25, fill=INK):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fill=RED, size=17):
    draw.text((x, y), text, font=font(SANS_B, size), fill=fill)
    return y + 24


def headline(draw, x, y, text, width, size=33, leading=40):
    fnt = font(SERIF_B, size)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def globe(draw, cx, cy, r):
    """A small line globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    draw.line([(cx - r + 8, cy - r // 2), (cx + r - 8, cy - r // 2)], fill=BLUE, width=1)
    draw.line([(cx - r + 8, cy + r // 2), (cx + r - 8, cy + r // 2)], fill=BLUE, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # ---- Masthead ----
    d.text((512, 14), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.text((512, 78), "FRIDAY  \u00b7  20 NOVEMBER 2026  \u00b7  ONE DAY, ONE PICTURE",
           font=font(SANS_B, 19), fill=RED, anchor="ma")
    rule(d, 28, 110, 996, 3)

    # ---- Lead: Shenzhen (left) + The Hague box (right) ----
    y = kicker(d, 28, 122, "SHENZHEN  \u00b7  THE TRILATERAL")
    y = headline(d, 28, y, "Trump, Putin and Xi issue a \u2018peace declaration\u2019", 600, 36, 44)
    y = para(d, 28, y + 4,
             "The three leaders hold first-ever trilateral talks at the APEC "
             "summit in Shenzhen. Sources call the declaration vague, with no "
             "significant agreements on Ukraine or nuclear arms \u2014 while "
             "Russian missiles are hitting bridges in Kyiv.",
             font(SANS, 18), 600, 24)
    rule(d, 28, 336, 996, 2)

    # ---- The Hague box ----
    d.rectangle([664, 122, 996, 326], outline=RED, width=3)
    y2 = kicker(d, 680, 134, "THE HAGUE  \u00b7  WORLD COURT", fill=RED, size=16)
    y2 = headline(d, 680, y2, "Myanmar guilty of genocide", 300, 26, 32)
    y2 = para(d, 680, y2 + 4,
              "The court finds Myanmar guilty of genocide against the "
              "Rohingya, 9\u20136 \u2014 the first such ruling in its "
              "80-year history.",
              font(SANS, 16), 300, 21)

    # ---- Three feature boxes ----
    boxes = [
        ("KYIV  \u00b7  OVERNIGHT STRIKES",
         "Russian missiles hit Kyiv bridges",
         "Three killed and nine injured as ballistic missiles strike "
         "several bridges and cut power."),
        ("NEW YORK  \u00b7  WALL STREET DEBUT",
         "Anthropic soars on Nasdaq debut",
         "The first purely AI company to list publicly: shares jump on "
         "day one, valuing the firm near $2 trillion."),
        ("WASHINGTON  \u00b7  CAPITOL AND COSTS",
         "Senate rejects Iran war-powers bid",
         "The resolution fails 51\u201348. The Pentagon puts the Iran war\u2019s "
         "cost at $48.3 billion; Trump pardons Pete Rose."),
    ]
    bx, bw, gap = 28, 310, 19
    for i, (kick, head, body) in enumerate(boxes):
        x0 = bx + i * (bw + gap)
        d.rectangle([x0, 352, x0 + bw, 566], outline=INK, width=2)
        yy = kicker(d, x0 + 14, 364, kick, fill=BLUE, size=14)
        yy = headline(d, x0 + 14, yy, head, bw - 28, 24, 30)
        para(d, x0 + 14, yy + 4, body, font(SANS, 16), bw - 28, 22)

    # ---- Three columns of short items ----
    rule(d, 28, 584, 996, 2)
    d.text((28, 594), "THE WORLD IN BRIEF", font=font(SANS_B, 18), fill=RED)
    cols = [
        ("EUROPE & THE WAR", [
            ("UK pledges 1,000+ drones for Ukraine", "in a \u00a3260m package of long-range kit."),
            ("Poland probes unknown objects", "after an air-threat warning is lifted."),
            ("Genoa airport halts flights", "after unidentified drones are seen."),
            ("UK and EU agree youth mobility", "in a rare summit, the BBC understands."),
            ("Harris meets Macron in Paris", "a courtesy meeting amid 2028 speculation."),
        ]),
        ("THE GULF & BEYOND", [
            ("Houthis claim four Saudi targets", "Saudi defences down two drones."),
            ("Tanker on fire after mine strike", "east of the Strait of Hormuz."),
            ("Israeli strike in east Lebanon", "hits a Hezbollah missile facility."),
            ("Gas blast kills six in Georgia", "in a Ponichala apartment block."),
            ("Quake of 5.6 near New Caledonia", "no tsunami warning follows."),
        ]),
        ("ALSO ON FRIDAY", [
            ("Fire in French tower block", "one dead, 15 injured, in 18 storeys."),
            ("Las Vegas GP practice washed out", "rain ruins the opening session."),
            ("Fiona the hippo dies", "at Cincinnati Zoo, after swallowing a hat."),
            ("US sanctions Comancheros", "and Italy\u2019s \u2019Ndrangheta crime group."),
            ("Argentina backs disability law", "its Senate votes 71\u20130."),
        ]),
    ]
    cx, cw = 28, 310
    for i, (title, items) in enumerate(cols):
        x0 = cx + i * (cw + 19)
        d.text((x0, 626), title, font=font(SANS_B, 16), fill=BLUE)
        yy = 652
        for head, tail in items:
            yy = para(d, x0, yy, "\u2022  " + head + " \u2014 " + tail,
                      font(SANS, 15), cw, 20)
            yy += 6

    # ---- Markets strip (Thursday's closes) ----
    d.rectangle([28, 894, 996, 962], fill=LIGHT, outline=INK, width=2)
    d.text((44, 902), "THURSDAY\u2019S MARKETS \u2014 WALL STREET SELLS OFF",
           font=font(SANS_B, 16), fill=RED)
    d.text((44, 924),
           "S&P 500  7,175.83  \u22122.02%      Dow  49,097.06  \u22122.19%      Nasdaq  23,879.20  \u22122.25%      VIX 28.44",
           font=font(SANS, 15), fill=INK)
    d.text((44, 944),
           "Gold  $3,685.50  \u22121.51%      Brent  $91.98  +0.03%      Bitcoin  ~$62,150  (Friday morning)",
           font=font(SANS, 15), fill=INK)

    # ---- Footer ----
    rule(d, 28, 974, 996, 2)
    d.text((28, 984),
           "Sources: AP, Reuters, BBC, Le Monde, Investopedia. Every story was reported on 20 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((28, 1002),
           "Drawn in code with Pillow  \u00b7  make.fun news-image-20261120",
           font=font(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
