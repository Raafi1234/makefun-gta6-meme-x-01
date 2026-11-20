#!/usr/bin/env python3
"""Compose the GTA 6 launch-week meme for the make.fun gta6-meme-x-01 entry.

Scene: a Vice City-flavoured neon boulevard at sunset (art/bg.png, drawn for
this entry) with make.fun's ghost mascot (art/mf-mark-1024.png, from
make.fun's own press kit) worked into the scene, holding its magenta coin.
Captions are rendered programmatically so the text stays sharp at any size.

Joke: after a 13-year wait for GTA 6, launch week is for playing - while the
reader's AI agent earns real money in make.fun bounties instead of waiting.

Run: python3 compose.py  ->  writes entry.png (1200x900) beside this file.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 900
TOP = "WAITED 13 YEARS FOR GTA 6"
BOTTOM_1 = "LAUNCH WEEK: I PLAY."
BOTTOM_2 = "MY AI AGENT GETS PAID ON make.fun"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 10:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(FONT_BOLD, size)


def caption(draw, center_x, y, text, font, fill=(255, 255, 255), stroke=(0, 0, 0), stroke_w=6):
    draw.text((center_x, y), text, font=font, fill=fill, anchor="ma",
              stroke_width=stroke_w, stroke_fill=stroke)


def main():
    bg = Image.open("art/bg.png").convert("RGB")
    # cover-crop the background to 1200x900
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * scale), round(bg.height * scale)))
    left = (bg.width - W) // 2
    top = (bg.height - H) // 2
    img = bg.crop((left, top, left + W, top + H)).convert("RGBA")

    # --- make.fun ghost, worked into the scene --------------------------------
    ghost = Image.open("art/mf-mark-1024.png").convert("RGBA")
    gw = 400
    ghost = ghost.resize((gw, round(ghost.height * gw / ghost.width)))
    gx, gy = W - gw - 90, 300
    # soft shadow so the ghost sits in the scene instead of floating on it
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh = ImageDraw.Draw(shadow)
    sh.ellipse([gx + 18, gy + ghost.height - 46, gx + gw - 18, gy + ghost.height + 6],
               fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, shadow)
    img.alpha_composite(ghost, (gx, gy))

    draw = ImageDraw.Draw(img)

    # --- captions --------------------------------------------------------------
    top_font = fit_font(draw, TOP, W - 80, 64)
    caption(draw, W // 2, 26, TOP, top_font)

    b1_font = fit_font(draw, BOTTOM_1, W - 80, 62)
    b2_font = fit_font(draw, BOTTOM_2, W - 80, 62)
    caption(draw, W // 2, H - 158, BOTTOM_1, b1_font)
    caption(draw, W // 2, H - 84, BOTTOM_2, b2_font, fill=(255, 110, 199))

    img.convert("RGB").save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
