#!/usr/bin/env python3
"""Compose the GTA 6 launch-week meme for the make.fun gta6-meme-x-01 entry.

Two-panel contrast, both panels drawn for this entry:
  LEFT  (art/left.png)  - a cobwebbed, forgotten game controller in a dim
                          room: the thirteen-year wait for GTA 6.
  RIGHT (art/right.png) - a Vice City-flavoured boulevard on launch night,
                          with make.fun's ghost mascot (art/mf-mark-1024.png,
                          from make.fun's own press kit) worked into the
                          scene as the round neon billboard on the hotel.
Captions are rendered programmatically so the text stays sharp at any size.

Joke: GTA 6 took so long that the player's AI agent learned to earn real
money on make.fun before the game even shipped.

Run: python3 compose.py  ->  writes entry.png (1200x900) beside this file.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 900
PANEL_H = 648
GAP = 8
PANEL_W = (W - GAP) // 2

LEFT_TOP = "2013-2025"
LEFT_SUB = "STILL WAITING FOR GTA 6..."
RIGHT_TOP = "2026"
RIGHT_SUB = "IT'S FINALLY OUT!"
BOTTOM_1 = "GOOD THING MY AI AGENT"
BOTTOM_2 = "ALREADY EARNS ON make.fun"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def cover(img, w, h):
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)))
    left = (img.width - w) // 2
    top = (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 10:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, size)


def caption(draw, cx, y, text, font, fill=(255, 255, 255), stroke_w=6):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma",
              stroke_width=stroke_w, stroke_fill=(0, 0, 0))


def main():
    canvas = Image.new("RGBA", (W, H), (10, 10, 18, 255))

    left = cover(Image.open("art/left.png").convert("RGB"), PANEL_W, PANEL_H).convert("RGBA")
    right = cover(Image.open("art/right.png").convert("RGB"), PANEL_W, PANEL_H).convert("RGBA")

    # --- make.fun ghost as the neon billboard on the right panel's hotel ------
    ghost = Image.open("art/mf-mark-1024.png").convert("RGBA")
    gw = 218
    ghost = ghost.resize((gw, round(ghost.height * gw / ghost.width)))
    gx, gy = 186, 96
    glow = Image.new("RGBA", right.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([gx - 16, gy - 16, gx + gw + 16, gy + ghost.height + 16],
               fill=(255, 0, 170, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    right = Image.alpha_composite(right, glow)
    right.alpha_composite(ghost, (gx, gy))

    canvas.alpha_composite(left, (0, 0))
    canvas.alpha_composite(right, (PANEL_W + GAP, 0))

    draw = ImageDraw.Draw(canvas)

    # --- panel captions ---------------------------------------------------------
    for x0, top_text, sub_text in ((0, LEFT_TOP, LEFT_SUB),
                                   (PANEL_W + GAP, RIGHT_TOP, RIGHT_SUB)):
        cx = x0 + PANEL_W // 2
        f_top = fit_font(draw, top_text, PANEL_W - 40, 54)
        f_sub = fit_font(draw, sub_text, PANEL_W - 40, 40)
        caption(draw, cx, PANEL_H - 118, top_text, f_top)
        caption(draw, cx, PANEL_H - 56, sub_text, f_sub, fill=(255, 214, 90))

    # --- bottom punchline ---------------------------------------------------------
    f1 = fit_font(draw, BOTTOM_1, W - 60, 66)
    f2 = fit_font(draw, BOTTOM_2, W - 60, 66)
    caption(draw, W // 2, PANEL_H + 26, BOTTOM_1, f1)
    caption(draw, W // 2, PANEL_H + 108, BOTTOM_2, f2, fill=(255, 110, 199))

    canvas.convert("RGB").save("entry.png")
    print("wrote entry.png", canvas.size)


if __name__ == "__main__":
    main()
