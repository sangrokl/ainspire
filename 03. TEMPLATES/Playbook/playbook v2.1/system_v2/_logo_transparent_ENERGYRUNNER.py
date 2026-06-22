# -*- coding: utf-8 -*-
# Luma-key the black-background VOLT logos to transparent PNGs for overlay.
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "projects", "energy-runner", "v20260621", "images", "logo")

def keyed(name):
    src = os.path.join(LOGO, name + ".png")
    if not os.path.exists(src):
        print("skip (missing)", name); return
    img = Image.open(src).convert("RGB")
    px = img.load()
    out = Image.new("RGBA", img.size)
    op = out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = max(r, g, b)              # brightness drives alpha
            a = 0 if lum < 16 else (255 if lum > 64 else int((lum - 16) / 48 * 255))
            op[x, y] = (r, g, b, a)
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    dst = os.path.join(LOGO, name + "_transparent.png")
    out.save(dst)
    print("saved", os.path.basename(dst), out.size)

for n in ["logo_v1", "logo_v2", "logo_v3", "logo_v4"]:
    keyed(n)
