#!/usr/bin/env python3
"""
video_pipeline.py
YouTube 영상 → 9:16 클립 → Whisper 자막 → Burn-in 최종 MP4

Usage:
    python3 video_pipeline.py <YouTube URL> <start_sec> <end_sec> [output_name]

Example:
    python3 video_pipeline.py "https://youtube.com/watch?v=xxxx" 10 25
    python3 video_pipeline.py "https://youtube.com/watch?v=xxxx" 10 25 my_clip
"""

import subprocess, sys, os, re, tempfile
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ── Paths ─────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_ROOT = os.path.join(BASE_DIR, "..", "..", "02. OUTPUTS")

# ── Subtitle Style Settings ───────────────────────────────────────────────
FONT_SIZE    = 40
MARGIN_B     = 200
PAD_X        = 16
PAD_Y        = 10
BOX_ALPHA    = 77       # 30% opacity (0~255)
BOX_RADIUS   = 4
LINE_SPACING = 8
FONT_COLOR   = (255, 255, 255, 255)
BOX_COLOR    = (0, 0, 0)

FONT_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]

# ── Whisper Settings ──────────────────────────────────────────────────────
WHISPER_MODEL    = "small"   # tiny / base / small / medium / large
WHISPER_LANGUAGE = "en"      # 영어: "en", 한국어: "ko", 자동감지: None
# ─────────────────────────────────────────────────────────────────────────


def run(cmd, label):
    print(f"\n[{label}]")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-600:])
        sys.exit(1)
    return result.stdout.strip()


def step1_download(url, tmpdir):
    """yt-dlp로 최고화질 MP4 다운로드."""
    out_tmpl = os.path.join(tmpdir, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", out_tmpl,
        url,
    ]
    print("\n[1/4] 다운로드 중...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-400:])
        sys.exit(1)

    mp4s = [f for f in os.listdir(tmpdir) if f.endswith(".mp4")]
    if not mp4s:
        print("다운로드 실패: MP4 파일을 찾을 수 없습니다.")
        sys.exit(1)
    path = os.path.join(tmpdir, mp4s[0])
    title = os.path.splitext(mp4s[0])[0]
    print(f"  → {mp4s[0]}")
    return path, title


def step2_crop_clip(input_mp4, start, end, tmpdir):
    """지정 구간 잘라서 9:16 크롭."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", input_mp4],
        capture_output=True, text=True,
    )
    W, H = [int(x) for x in probe.stdout.strip().split(",")]
    crop_w = int(H * 9 / 16)
    if crop_w % 2:
        crop_w -= 1
    crop_x = (W - crop_w) // 2

    out = os.path.join(tmpdir, "clip_9x16.mp4")
    print(f"\n[2/4] 크롭 & 트림 ({start}s ~ {end}s, {crop_w}x{H} 9:16)...")
    cmd = [
        "ffmpeg", "-y",
        "-i", input_mp4,
        "-ss", str(start), "-to", str(end),
        "-vf", f"crop={crop_w}:{H}:{crop_x}:0",
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        "-c:a", "aac", "-b:a", "192k",
        out,
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"  → {out}")
    return out, crop_w, H


def step3_whisper(clip_mp4, tmpdir):
    """Whisper로 자막 생성 → SRT 반환."""
    print(f"\n[3/4] Whisper 자막 생성 (model={WHISPER_MODEL})...")
    cmd = [
        "whisper", clip_mp4,
        "--model", WHISPER_MODEL,
        "--output_format", "srt",
        "--output_dir", tmpdir,
    ]
    if WHISPER_LANGUAGE:
        cmd += ["--language", WHISPER_LANGUAGE]
    subprocess.run(cmd, capture_output=True)

    base = os.path.splitext(os.path.basename(clip_mp4))[0]
    srt  = os.path.join(tmpdir, base + ".srt")
    if not os.path.exists(srt):
        print("  자막 파일 생성 실패.")
        sys.exit(1)
    # count entries
    count = len(re.findall(r"^\d+$", open(srt).read(), re.MULTILINE))
    print(f"  → {count}개 자막 항목")
    return srt


def parse_srt(path):
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
        subs.append((start, end, "\n".join(lines[2:])))
    return subs


def render_sub(text, W, H, font):
    img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    lines   = text.split("\n")
    line_h  = FONT_SIZE + LINE_SPACING
    total_h = len(lines) * line_h - LINE_SPACING
    y_start = H - MARGIN_B - total_h

    max_tw = max(
        draw.textbbox((0,0), ln, font=font)[2] - draw.textbbox((0,0), ln, font=font)[0]
        for ln in lines
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

    for li, ln in enumerate(lines):
        bb = draw.textbbox((0, 0), ln, font=font)
        tw = bb[2] - bb[0]
        x  = (W - tw) // 2
        y  = y_start + li * line_h
        draw.text((x, y), ln, font=font, fill=FONT_COLOR)
    return img


def step4_burn(clip_mp4, srt_path, output_mp4, W, H):
    """자막 PNG overlay → 최종 MP4."""
    print(f"\n[4/4] 자막 burn-in...")
    subs = parse_srt(srt_path)

    font = None
    for p in FONT_PATHS:
        if os.path.exists(p):
            font = ImageFont.truetype(p, FONT_SIZE)
            break
    if font is None:
        font = ImageFont.load_default()

    tmpdir = tempfile.mkdtemp()
    png_paths = []
    for i, (s, e, txt) in enumerate(subs):
        p = os.path.join(tmpdir, f"sub_{i:02d}.png")
        render_sub(txt, W, H, font).save(p)
        png_paths.append((s, e, p))

    inputs = ["-i", clip_mp4]
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
    if result.returncode != 0:
        print(result.stderr[-600:])
        sys.exit(1)
    size = os.path.getsize(output_mp4) / 1024 / 1024
    print(f"  → {output_mp4} ({size:.1f} MB)")


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    url        = sys.argv[1]
    start_sec  = float(sys.argv[2])
    end_sec    = float(sys.argv[3])
    label      = sys.argv[4] if len(sys.argv) > 4 else "clip"
    safe_label = re.sub(r"[^\w\-]", "_", label)

    # YYYYMMDD_프로젝트명 폴더 생성
    date_prefix = datetime.now().strftime("%Y%m%d")
    folder_name = f"{date_prefix}_{safe_label}"
    OUTPUTS_DIR = os.path.join(OUTPUTS_ROOT, folder_name)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    tmpdir = tempfile.mkdtemp()

    print("=" * 50)
    print(f"  URL   : {url}")
    print(f"  구간   : {start_sec}s ~ {end_sec}s")
    print(f"  폴더   : 02. OUTPUTS/{folder_name}/")
    print("=" * 50)

    src_mp4, _      = step1_download(url, tmpdir)
    clip_mp4, W, H  = step2_crop_clip(src_mp4, start_sec, end_sec, tmpdir)
    srt_path        = step3_whisper(clip_mp4, tmpdir)

    import shutil
    srt_out = os.path.join(OUTPUTS_DIR, f"{safe_label}.srt")
    shutil.copy(srt_path, srt_out)

    final_mp4 = os.path.join(OUTPUTS_DIR, f"{safe_label}_final.mp4")
    step4_burn(clip_mp4, srt_path, final_mp4, W, H)

    print("\n" + "=" * 50)
    print("  완료!")
    print(f"  영상 : 02. OUTPUTS/{folder_name}/{safe_label}_final.mp4")
    print(f"  자막 : 02. OUTPUTS/{folder_name}/{safe_label}.srt")
    print("=" * 50)


if __name__ == "__main__":
    main()
