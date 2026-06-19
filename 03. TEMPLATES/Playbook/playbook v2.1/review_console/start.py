# -*- coding: utf-8 -*-
"""
원클릭 실행기: 콘솔 HTML 빌드 → 로컬 서버 기동 → 큐 워처 기동 → 브라우저 자동 오픈.

예)
  python start.py --media-dir "../projects/commercial/aether_energy/v2026-05-29_v4" --mode image --title "AETHER 스토리보드 리뷰"
  python start.py --media-dir "../projects/.../videos/seedance" --mode video --title "HALO 영상 리뷰"

★ 모든 생성은 Higgsfield MCP 전용. 실제 재생성은 Claude 에이전트가 큐를 받아 처리(AGENT_QUEUE_GUIDE).
백엔드 선택:  --backend mock(기본·오프라인 UI 데모) | agent(실가동 — Higgsfield MCP, Claude 에이전트 처리)
"""
import argparse, os, subprocess, sys, time, webbrowser
from pathlib import Path

PKG = Path(__file__).resolve().parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-dir", required=True, help="이미지/영상 폴더")
    ap.add_argument("--mode", choices=["image", "video"], default="image")
    ap.add_argument("--title", default="리뷰 콘솔")
    ap.add_argument("--accent", default="#3aa0ff")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--backend", choices=["mock", "agent"], default="mock",
                    help="mock=오프라인 데모 / agent=실가동(Higgsfield MCP, Claude 에이전트가 큐 처리)")
    ap.add_argument("--no-worker", action="store_true")
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()

    media = str(Path(a.media_dir).resolve())
    webroot = PKG / "webroot"; webroot.mkdir(exist_ok=True)
    runtime = PKG / "runtime"; runtime.mkdir(exist_ok=True)
    # 세션마다 큐/결과 초기화
    (runtime / "revision_queue.jsonl").write_text("", encoding="utf-8")
    (runtime / "results.json").write_text("{}", encoding="utf-8")
    (runtime / ".queue_offset").write_text("0", encoding="utf-8")

    subprocess.run([sys.executable, str(PKG / "build_console.py"),
                    "--media-dir", media, "--mode", a.mode, "--title", a.title,
                    "--accent", a.accent, "--out", str(webroot / "console.html")], check=True)

    env = dict(os.environ, PORT=str(a.port), MEDIA_DIR=media,
               WEBROOT=str(webroot), RUNTIME=str(runtime), BACKEND=a.backend)
    server = subprocess.Popen([sys.executable, str(PKG / "review_server.py")], env=env)
    worker = None
    if not a.no_worker:
        worker = subprocess.Popen([sys.executable, str(PKG / "worker.py")], env=env)

    if not a.no_open:
        time.sleep(1.0)
        webbrowser.open(f"http://localhost:{a.port}/")
    print(f"\n  ▶ 리뷰 콘솔: http://localhost:{a.port}/   (backend={a.backend})")
    print("  종료: Ctrl+C\n")
    try:
        server.wait()
    except KeyboardInterrupt:
        pass
    finally:
        server.terminate()
        if worker:
            worker.terminate()


if __name__ == "__main__":
    main()
