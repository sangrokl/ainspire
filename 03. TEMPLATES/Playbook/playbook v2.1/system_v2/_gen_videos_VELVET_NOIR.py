#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VELVET NOIR — 30컷 배치 비디오 생성
Usage:
  python3 system_v2/_gen_videos_VELVET_NOIR.py submit   # 30개 잡 한꺼번에 제출
  python3 system_v2/_gen_videos_VELVET_NOIR.py poll     # 완료 확인 + 다운로드
  python3 system_v2/_gen_videos_VELVET_NOIR.py run      # submit → poll (직접 실행)
"""
import argparse, json, re, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT     = Path(__file__).parent.parent
VD       = ROOT / "projects" / "VELVET_NOIR" / "v20260626"
SCENARIO = VD / "assets" / "md" / "scenario.md"
IMG_DIR  = VD / "assets" / "images"
VID_DIR  = VD / "assets" / "videos"
JOBS_JSON= VD / "assets" / "md" / "_video_jobs.json"

MODEL      = "kling3_0_turbo"
RESOLUTION = "1080p"
DURATION   = 4
ASPECT     = "16:9"

RULE0_VIDEO = (
    "COMPOSITION RULES — apply without exception: "
    "ZERO front-facing, ZERO eye-level. Subject NEVER looks into lens. "
    "DUTCH / HIGH / LOW angle only. Hard warm BACKLIGHT tracing subject silhouette. "
    "BLACK NEGATIVE FILL on shadow side. LOW-KEY only."
)

VIDEO_AUDIO = (
    "AUDIO: NO background music, NO score, NO BGM. "
    "Diegetic SFX ONLY — ambient room tone, natural sound, foley. "
    "Silence is preferred over any music."
)

# ── Parse scenario.md ─────────────────────────────────────────────────────────

def parse_video_prompts():
    txt = SCENARIO.read_text(encoding="utf-8")
    cuts = {}
    for m in re.finditer(r'## Cut (\d+)\n(.*?)(?=\n## Cut \d+|\Z)', txt, re.DOTALL):
        n    = int(m.group(1))
        body = m.group(2)
        vp   = re.search(r'\[video prompt\]:\s*(.+?)(?=\n\[|\Z)', body, re.DOTALL)
        if vp:
            cuts[n] = vp.group(1).strip()
    return cuts

# ── CLI helpers ───────────────────────────────────────────────────────────────

def submit_job(cut_n: int, video_prompt: str) -> str:
    """Submit one video job without --wait; returns job_id."""
    img_path = IMG_DIR / f"cut_{cut_n:02d}.png"
    full_prompt = RULE0_VIDEO + "\n\n" + VIDEO_AUDIO + "\n\n" + video_prompt

    cmd = [
        "higgsfield", "generate", "create", MODEL,
        "--prompt", full_prompt,
        "--aspect_ratio", ASPECT,
        "--duration", str(DURATION),
        "--resolution", RESOLUTION,
        "--json",
    ]
    if img_path.exists():
        cmd += ["--start-image", str(img_path)]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    raw = result.stdout.strip()
    if result.returncode != 0 and not raw:
        raise RuntimeError(f"CUT {cut_n:02d} submit failed: {result.stderr}")

    # Response is either ["job_id"] or {"id": "..."}
    data = json.loads(raw)
    if isinstance(data, list):
        return data[0]
    if isinstance(data, dict):
        return data.get("id") or data.get("job_id") or str(data)
    return str(data)


def poll_job(job_id: str):
    """Poll a single job; returns (status_str, result_url_or_None)."""
    cmd = ["higgsfield", "generate", "get", job_id, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    raw = result.stdout.strip()
    if not raw:
        return "unknown", None
    matches = re.findall(r'\{[\s\S]+\}', raw)
    if not matches:
        return "unknown", None
    data = json.loads(matches[-1])

    status = (data.get("status") or "").lower()
    url = None
    for k in ("result_url", "rawUrl", "url", "videoUrl", "video_url"):
        if k in data and isinstance(data[k], str) and data[k].startswith("http"):
            url = data[k]
            break
    if not url and isinstance(data.get("results"), list):
        for item in data["results"]:
            if isinstance(item, dict):
                for k in ("url", "rawUrl", "result_url"):
                    if k in item and isinstance(item[k], str) and item[k].startswith("http"):
                        url = item[k]
                        break
            if url:
                break
    return status, url


def download(url: str, path: Path):
    urllib.request.urlretrieve(url, path)

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_submit(cuts_filter=None):
    VID_DIR.mkdir(parents=True, exist_ok=True)
    prompts = parse_video_prompts()
    targets = sorted(prompts.keys())
    if cuts_filter:
        targets = [n for n in targets if n in cuts_filter]

    # Load existing jobs to skip already-submitted cuts
    existing = {}
    if JOBS_JSON.exists():
        existing = json.loads(JOBS_JSON.read_text())

    jobs = dict(existing)

    print(f"\n  ▐ VELVET NOIR 영상 배치 제출  ({len(targets)} cuts / {MODEL})")
    print(f"  해상도: {RESOLUTION} | 길이: {DURATION}s | 시작프레임: cut_XX.png\n")

    for n in targets:
        key = str(n)
        if key in jobs:
            print(f"  CUT {n:02d}  SKIP  (이미 제출됨: {jobs[key]['job_id']})")
            continue
        try:
            job_id = submit_job(n, prompts[n])
            jobs[key] = {"job_id": job_id, "status": "pending", "url": None}
            JOBS_JSON.write_text(json.dumps(jobs, ensure_ascii=False, indent=2))
            print(f"  CUT {n:02d}  ✓ submitted  {job_id}")
        except Exception as e:
            print(f"  CUT {n:02d}  ✗ ERROR: {e}")

    print(f"\n  잡 목록 저장: {JOBS_JSON}")
    print(f"  완료 확인: python3 system_v2/_gen_videos_VELVET_NOIR.py poll\n")


def cmd_poll():
    if not JOBS_JSON.exists():
        print("  잡 목록 없음 — 먼저 submit 실행하세요")
        sys.exit(1)

    VID_DIR.mkdir(parents=True, exist_ok=True)
    jobs = json.loads(JOBS_JSON.read_text())
    total     = len(jobs)
    done_set  = set()
    error_set = set()

    print(f"\n  ▐ VELVET NOIR 영상 폴링  ({total} jobs)\n")

    while True:
        pending = {k: v for k, v in jobs.items()
                   if v["status"] not in ("completed", "failed")}
        if not pending:
            break

        for key, info in list(pending.items()):
            n      = int(key)
            jid    = info["job_id"]
            status, url = poll_job(jid)
            jobs[key]["status"] = status

            out = VID_DIR / f"cut_{n:02d}.mp4"

            if status in ("completed", "succeeded") and url:
                if not out.exists():
                    try:
                        download(url, out)
                        size = out.stat().st_size // 1024
                        print(f"  CUT {n:02d}  ✓ {size} KB  {out.name}")
                    except Exception as e:
                        print(f"  CUT {n:02d}  ✗ download error: {e}")
                        jobs[key]["status"] = "failed"
                        error_set.add(n)
                        continue
                jobs[key]["status"] = "completed"
                jobs[key]["url"]    = url
                done_set.add(n)
            elif status in ("failed", "error"):
                print(f"  CUT {n:02d}  ✗ FAILED  {jid}")
                jobs[key]["status"] = "failed"
                error_set.add(n)
            else:
                print(f"  CUT {n:02d}  ⏳ {status or 'pending'}")

        JOBS_JSON.write_text(json.dumps(jobs, ensure_ascii=False, indent=2))

        still_pending = sum(1 for v in jobs.values() if v["status"] not in ("completed", "failed"))
        print(f"\n  완료 {len(done_set)}/{total} | 실패 {len(error_set)} | 대기 {still_pending}")

        if still_pending == 0:
            break

        print(f"  30초 후 재확인…\n")
        time.sleep(30)

    # Final summary
    completed = [k for k, v in jobs.items() if v["status"] == "completed"]
    failed    = [k for k, v in jobs.items() if v["status"] == "failed"]
    print(f"\n  ─────────────────────────────────────────")
    print(f"  완료: {len(completed)}/{total}컷")
    if failed:
        print(f"  실패 컷: {sorted(int(k) for k in failed)}")
        print(f"  재시도: python3 system_v2/_gen_videos_VELVET_NOIR.py submit --cuts {','.join(str(int(k)) for k in failed)}")
    print(f"  영상 저장: {VID_DIR}\n")


def cmd_run():
    cmd_submit()
    print("  모든 잡 제출 완료 → 폴링 시작 (30초 간격)\n")
    time.sleep(5)
    cmd_poll()


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["submit", "poll", "run"])
    ap.add_argument("--cuts", help="comma-separated cut numbers, e.g. 1,3,5")
    args = ap.parse_args()

    cuts_filter = None
    if args.cuts:
        cuts_filter = set(int(x.strip()) for x in args.cuts.split(","))

    if args.command == "submit":
        cmd_submit(cuts_filter)
    elif args.command == "poll":
        cmd_poll()
    elif args.command == "run":
        cmd_run()
