#!/usr/bin/env python3
"""
subtitle_burner.py
SRT 자막을 영상에 burn-in하는 재사용 스크립트.

Usage:
    python3 subtitle_burner.py input.mp4 subtitles.srt output.mp4
"""

import subprocess, sys, os, re, tempfile
from PIL import Image, ImageDraw, ImageFont

# ── Style Settings ────────────────────────────────────────────────────────
FONT_SIZE   = 40        # px
MARGIN_B    = 200       # px from bottom
PAD_X       = 16        # box horizontal padding
PAD_Y       = 10        # box vertical padding
BOX_ALPHA   = 77        # box opacity: 0=투명 ~ 255=불투명 (30% = 77)
BOX_RADIUS  = 4         # box corner radius px
LINE_SPACING = 8        # extra px between lines
FONT_COLOR  = (255, 255, 255, 255)   # white
BOX_COLOR   = (0, 0, 0)             # black

FONT_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
# ─────────────────────────────────────────────────────────────────────────


def load_font(size):
    for p in FONT_PATHS:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def parse_srt(path):
    """Returns list of (start_sec, end_sec, text)."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    subs = []
    for block in re.split(r"\n\n+", content.strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            lines[1],
        )
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        start = g[0]*3600 + g[1]*60 + g[2] + g[3]/1000
        end   = g[4]*3600 + g[5]*60 + g[6] + g[7]/1000
        text  = "\n".join(lines[2:])
        subs.append((start, end, text))
    return subs


def render_sub(text, W, H, font):
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines   = text.split("\n")
    line_h  = FONT_SIZE + LINE_SPACING
    total_h = len(lines) * line_h - LINE_SPACING
    y_start = H - MARGIN_B - total_h

    max_tw = max(
        draw.textbbox((0,0), line, font=font)[2] - draw.textbbox((0,0), line, font=font)[0]
        for line in lines
    )
    bx1 = (W - max_tw) // 2 - PAD_X
    by1 = y_start - PAD_Y
    bx2 = (W + max_tw) // 2 + PAD_X
    by2 = y_start + total_h + PAD_Y

    overlay  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    box_draw = ImageDraw.Draw(overlay)
    box_draw.rounded_rectangle(
        [bx1, by1, bx2, by2],
        radius=BOX_RADIUS,
        fill=(*BOX_COLOR, BOX_ALPHA),
    )
    img  = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    for li, line in enumerate(lines):
        bb = draw.textbbox((0, 0), line, font=font)
        tw = bb[2] - bb[0]
        x  = (W - tw) // 2
        y  = y_start + li * line_h
        draw.text((x, y), line, font=font, fill=FONT_COLOR)
    return img


def burn_subtitles(input_mp4, srt_path, output_mp4):
    # video dimensions
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", input_mp4],
        capture_output=True, text=True,
    )
    W, H = [int(x) for x in probe.stdout.strip().split(",")]
    print(f"영상 크기: {W}x{H}")

    subs = parse_srt(srt_path)
    font = load_font(FONT_SIZE)
    tmpdir = tempfile.mkdtemp()

    png_paths = []
    for i, (s, e, txt) in enumerate(subs):
        p = os.path.join(tmpdir, f"sub_{i:02d}.png")
        render_sub(txt, W, H, font).save(p)
        png_paths.append((s, e, p))
        print(f"  [{s:.2f}s-{e:.2f}s] {txt!r}")

    inputs = ["-i", input_mp4]
    for _, _, p in png_paths:
        inputs += ["-i", p]

    filter_parts = []
    prev = "0:v"
    for i, (s, e, _) in enumerate(png_paths):
        out = f"ov{i}"
        filter_parts.append(
            f"[{prev}][{i+1}:v]overlay=0:0:enable='between(t,{s},{e})'[{out}]"
        )
        prev = out

    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex", ";".join(filter_parts),
            "-map", f"[{prev}]",
            "-map", "0:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-c:a", "copy",
            output_mp4,
        ]
    )

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(output_mp4) / 1024 / 1024
        print(f"\n완료: {output_mp4} ({size:.1f} MB)")
    else:
        print(result.stderr[-800:])
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 subtitle_burner.py input.mp4 subtitles.srt output.mp4")
        sys.exit(1)
    burn_subtitles(sys.argv[1], sys.argv[2], sys.argv[3])
