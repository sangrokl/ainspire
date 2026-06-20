# -*- coding: utf-8 -*-
# Luma-key the black-background TETHER logos to transparent PNGs, then auto-crop.
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "projects", "tether", "v20260620_v3", "images", "logo")


def keyed(name):
    src = os.path.join(LOGO, name + ".png")
    if not os.path.exists(src):
        print("skip (missing)", name)
        return
    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(np.int32)
    lum = arr.max(axis=2)  # brightness drives alpha
    alpha = np.clip((lum.astype(np.float32) - 16) / 48 * 255, 0, 255).astype(np.uint8)
    alpha[lum < 16] = 0
    alpha[lum > 64] = 255
    out_arr = np.dstack([arr.astype(np.uint8), alpha])
    out = Image.fromarray(out_arr, mode="RGBA")

    bbox = out.getbbox()
    if bbox:
        pad = 24
        l, t, r, b = bbox
        l = max(0, l - pad)
        t = max(0, t - pad)
        r = min(out.width, r + pad)
        b = min(out.height, b + pad)
        out = out.crop((l, t, r, b))

    dst = os.path.join(LOGO, name + "_transparent.png")
    out.save(dst)
    print("saved", os.path.basename(dst), out.size)


for n in ["logo_v1", "logo_v2", "logo_v3", "logo_v4"]:
    keyed(n)
