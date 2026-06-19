# -*- coding: utf-8 -*-
"""
큐 워처 — revision_queue.jsonl 을 읽어 항목별 상태를 results.json 에 반영한다.

★ 모든 실제 생성은 Higgsfield MCP 전용 (이미지: nano_banana_2 / gpt_image_2,  영상: seedance_2_0).
   Higgsfield MCP 는 Claude 에이전트만 호출할 수 있으므로, 이 워커는 직접 생성하지 않는다.

백엔드(BACKEND 환경변수):
  - mock  : (기본·오프라인 데모) 원본에 '수정본' 라벨을 얹어 _revisions/ 에 저장. 키·MCP 불필요.
  - agent : (실가동) 항목을 'needs-agent'로 표시만 한다. 실제 재생성은 Claude 에이전트가
            AGENT_QUEUE_GUIDE.md 대로 Higgsfield MCP(generate_image / generate_video)로 처리하고
            results.json 을 done 으로 갱신한다.

설정: 환경변수 MEDIA_DIR, RUNTIME, BACKEND  또는 같은 폴더의 config.json
"""
import json, os, time
from pathlib import Path

PKG = Path(__file__).resolve().parent
CFG = {}
if (PKG / "config.json").exists():
    CFG = json.loads((PKG / "config.json").read_text(encoding="utf-8"))

MEDIA_DIR = Path(os.environ.get("MEDIA_DIR") or CFG.get("media_dir", PKG / "media")).resolve()
RUNTIME = Path(os.environ.get("RUNTIME") or CFG.get("runtime", PKG / "runtime")).resolve()
RUNTIME.mkdir(parents=True, exist_ok=True)
QUEUE = RUNTIME / "revision_queue.jsonl"
RESULTS = RUNTIME / "results.json"
OFFSET = RUNTIME / ".queue_offset"
REV = MEDIA_DIR / "_revisions"; REV.mkdir(exist_ok=True)

BACKEND = (os.environ.get("BACKEND") or CFG.get("backend", "mock")).lower()
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
VID_EXT = (".mp4", ".webm", ".mov")


def load_results():
    return json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}

def set_result(cut, **kw):
    r = load_results(); r[cut] = {**r.get(cut, {}), **kw, "ts": int(time.time())}
    RESULTS.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")

def find_original(cut):
    for ext in IMG_EXT + VID_EXT:
        p = MEDIA_DIR / (cut + ext)
        if p.exists():
            return p
    return None

def next_rev_path(cut, ext):
    k = 1
    while (REV / f"{cut}_rev{k}{ext}").exists():
        k += 1
    return REV / f"{cut}_rev{k}{ext}"


# ---------- mock backend (offline UI demo only) ----------
def do_mock(item):
    from PIL import Image, ImageDraw
    cut = item["cut"]; src = find_original(cut)
    if not src:
        return set_result(cut, status="error", msg="원본 없음")
    time.sleep(2)
    if src.suffix.lower() in VID_EXT:
        out = next_rev_path(cut, src.suffix); out.write_bytes(src.read_bytes())
        return set_result(cut, status="done", src="/media/_revisions/" + out.name, msg="mock")
    img = Image.open(src).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, img.height - 84, img.width, img.height], fill=(10, 12, 18, 200))
    d.text((18, img.height - 64), f"수정본 · {item.get('request','')[:40]}", fill=(90, 224, 160, 255))
    model = item.get("model") or ("seedance_2_0" if item.get("type") == "video" else "-")
    d.text((18, img.height - 38), f"[mock] Higgsfield {model} · q={item.get('quality','-')}",
           fill=(174, 182, 200, 255))
    out = next_rev_path(cut, ".png"); img.save(out)
    set_result(cut, status="done", src="/media/_revisions/" + out.name, msg="mock")


def process(item):
    t = item.get("type"); cut = item.get("cut", "")
    if t == "batch_video":
        return set_result("_batch", status="running",
                          msg="전체 영상화 요청 — Claude 에이전트가 Higgsfield seedance_2_0 로 처리(AGENT_QUEUE_GUIDE)")
    if BACKEND == "mock":
        set_result(cut, status="running")
        return do_mock(item)
    # agent(실가동): Higgsfield MCP 전용 → Claude 에이전트가 처리. 워커는 표시만.
    model = item.get("model") or ("seedance_2_0" if t == "video" else "nano_banana_2")
    set_result(cut, status="running", needs_agent=True,
               msg=f"Higgsfield {model} 대기 — Claude 에이전트가 처리")


def main():
    print(f"[worker] backend={BACKEND} (generation=Higgsfield MCP only) media={MEDIA_DIR}")
    off = int(OFFSET.read_text()) if OFFSET.exists() else 0
    while True:
        if QUEUE.exists():
            lines = QUEUE.read_text(encoding="utf-8").splitlines()
            while off < len(lines):
                line = lines[off].strip(); off += 1; OFFSET.write_text(str(off))
                if not line:
                    continue
                try:
                    item = json.loads(line)
                    print("[worker] queue:", item.get("type"), item.get("cut", ""), "model=", item.get("model", "-"))
                    process(item)
                except Exception as e:
                    print("[worker] err", str(e)[:120])
        time.sleep(1.5)


if __name__ == "__main__":
    main()
