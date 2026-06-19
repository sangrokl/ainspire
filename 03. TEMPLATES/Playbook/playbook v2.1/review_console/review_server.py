# -*- coding: utf-8 -*-
"""
리뷰 콘솔 로컬 서버 (파이썬 표준 라이브러리만).
- GET  /            -> webroot/console.html
- GET  /media/<f>   -> MEDIA_DIR 의 파일 (썸네일/영상/수정본)
- GET  /results     -> runtime/results.json (콘솔이 4초마다 폴링)
- POST /revise      -> runtime/revision_queue.jsonl 에 요청 한 줄 append

설정(환경변수): PORT, MEDIA_DIR, WEBROOT, RUNTIME
"""
import http.server, json, os, mimetypes, urllib.parse
from pathlib import Path

PKG = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", "8765"))
MEDIA_DIR = Path(os.environ.get("MEDIA_DIR", PKG / "media")).resolve()
WEBROOT = Path(os.environ.get("WEBROOT", PKG / "webroot")).resolve()
RUNTIME = Path(os.environ.get("RUNTIME", PKG / "runtime")).resolve()
RUNTIME.mkdir(parents=True, exist_ok=True)
QUEUE = RUNTIME / "revision_queue.jsonl"
RESULTS = RUNTIME / "results.json"


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p in ("/", "/index.html"):
            f = WEBROOT / "console.html"
            return self._send(200, "text/html; charset=utf-8",
                              f.read_bytes() if f.exists() else b"console not built")
        if p == "/results":
            return self._send(200, "application/json",
                              RESULTS.read_bytes() if RESULTS.exists() else b"{}")
        if p.startswith("/media/"):
            rel = urllib.parse.unquote(p[len("/media/"):])
            target = (MEDIA_DIR / rel).resolve()
            try:
                target.relative_to(MEDIA_DIR)  # path-traversal 방지
            except ValueError:
                return self._send(403, "text/plain", b"forbidden")
            if target.is_file():
                ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
                return self._send(200, ctype, target.read_bytes())
            return self._send(404, "text/plain", b"not found")
        return self._send(404, "text/plain", b"not found")

    def do_POST(self):
        p = urllib.parse.urlparse(self.path).path
        if p == "/revise":
            n = int(self.headers.get("Content-Length", "0") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except Exception:
                return self._send(400, "application/json", b'{"ok":false}')
            with open(QUEUE, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(body, ensure_ascii=False) + "\n")
            return self._send(200, "application/json", b'{"ok":true}')
        return self._send(404, "text/plain", b"not found")

    def log_message(self, *a):
        pass  # 콘솔 조용히


def main():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"[review_server] http://localhost:{PORT}/  media={MEDIA_DIR}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
