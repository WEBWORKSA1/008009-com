#!/usr/bin/env python3
"""Generate favicon.svg, PWA icons and the Open Graph image (run in CI)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from layout import LOGO_SVG
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = os.path.join(ROOT, "assets", "img"); os.makedirs(IMG, exist_ok=True)
open(os.path.join(IMG, "favicon.svg"), "w").write(LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ''))
def font(sz, bold=True):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"]:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    try: return ImageFont.load_default(size=sz)
    except Exception: return ImageFont.load_default()
def icon(n):
    im = Image.new("RGB", (n, n), "#B3131B"); d = ImageDraw.Draw(im); w = max(4, n // 13)
    d.ellipse([n*.34, n*.18, n*.66, n*.5], outline="#C9A227", width=w)
    d.ellipse([n*.31, n*.46, n*.69, n*.84], outline="#C9A227", width=w)
    im.save(os.path.join(IMG, f"icon-{n}.png"))
icon(192); icon(512)
W, H = 1200, 630
im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
for i in range(H):
    c = int(0x8E + (0xB3 - 0x8E) * i / H); d.line([(0, i), (W, i)], fill=(c, 0x10, 0x18))
d.rectangle([24, 24, W-24, H-24], outline="#C9A227", width=6)
d.text((W/2, 200), "008 · 009", font=font(150), fill="#FFFFFF", anchor="mm")
d.text((W/2, 340), "LUCKY NUMBERS HUB", font=font(52), fill="#C9A227", anchor="mm")
d.text((W/2, 440), "Free Chinese numerology tools · Number meanings", font=font(34, False), fill="#fde7e8", anchor="mm")
d.text((W/2, 490), "Lucky Number Exchange: phones · plates · domains", font=font(34, False), fill="#fde7e8", anchor="mm")
d.text((W/2, 570), "008009.com", font=font(40), fill="#C9A227", anchor="mm")
im.save(os.path.join(IMG, "og-image.png"), optimize=True)
print("images ok")
