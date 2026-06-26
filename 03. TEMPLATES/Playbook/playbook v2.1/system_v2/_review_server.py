#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Higgsfield Interactive Review Server
Usage: python3 system_v2/_review_server.py [--project VELVET_NOIR] [--version v20260626] [--port 7800]
Then open: http://localhost:7800
"""
import argparse, base64, json, mimetypes, os, re, subprocess
import threading, urllib.request, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Private-Network": "true",   # Chrome PNA policy
}


# ── CLI runners ──────────────────────────────────────────────────────────────

def _run_cli(cmd, timeout=1200):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    raw = result.stdout.strip()
    if result.returncode != 0 and not raw:
        raise RuntimeError(result.stderr or "CLI returned no output")
    # Extract last JSON block (CLI may emit progress lines before the result)
    matches = re.findall(r'\{[\s\S]+\}', raw)
    if not matches:
        raise RuntimeError(f"No JSON in CLI output:\n{raw}\n{result.stderr}")
    return json.loads(matches[-1])


def _extract_url(data):
    """Recursively find a media URL in CLI JSON response."""
    if isinstance(data, dict):
        for k in ("rawUrl", "url", "videoUrl", "imageUrl", "video_url", "image_url"):
            if k in data and isinstance(data[k], str) and data[k].startswith("http"):
                return data[k]
        for v in data.values():
            r = _extract_url(v)
            if r:
                return r
    elif isinstance(data, list):
        for item in data:
            r = _extract_url(item)
            if r:
                return r
    return None


def regen_image(prompt, model, resolution="2k", aspect_ratio="16:9"):
    cmd = [
        "higgsfield", "generate", "create", model,
        "--prompt", prompt,
        "--aspect_ratio", aspect_ratio,
        "--resolution", resolution,
        "--wait", "--wait-timeout", "10m", "--wait-interval", "3s",
        "--json",
    ]
    data = _run_cli(cmd, timeout=700)
    url = _extract_url(data)
    if not url:
        raise RuntimeError(f"No URL found in CLI response: {json.dumps(data)[:400]}")
    return url


def regen_video(prompt, model, duration=5, resolution="1080p", aspect_ratio="16:9"):
    cmd = [
        "higgsfield", "generate", "create", model,
        "--prompt", prompt,
        "--aspect_ratio", aspect_ratio,
        "--duration", str(duration),
        "--resolution", resolution,
        "--wait", "--wait-timeout", "20m", "--wait-interval", "5s",
        "--json",
    ]
    data = _run_cli(cmd, timeout=1300)
    url = _extract_url(data)
    if not url:
        raise RuntimeError(f"No URL found in CLI response: {json.dumps(data)[:400]}")
    return url


# ── HTTP Handler ─────────────────────────────────────────────────────────────

class ReviewHandler(BaseHTTPRequestHandler):
    project = "VELVET_NOIR"
    version = "v20260626"

    def vdir(self):
        return ROOT / "projects" / self.project / self.version

    def log_message(self, fmt, *args):
        print(f"  [{self.address_string()}] {fmt % args}")

    def _send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path):
        path = Path(path)
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", len(data))
        self.send_header("Cache-Control", "no-cache")
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_GET(self):
        p = self.path.split("?")[0]
        vd = self.vdir()

        if p in ("/", "/index.html"):
            html = vd / "preview" / f"storyboard_{self.project}_30cut_{self.version}.html"
            self._send_file(html)
        elif p.startswith("/api/images/"):
            self._send_file(vd / "assets" / "images" / p[len("/api/images/"):])
        elif p.startswith("/api/videos/"):
            self._send_file(vd / "assets" / "videos" / p[len("/api/videos/"):])
        elif p == "/api/status":
            self._send_json(200, {"ok": True, "project": self.project, "version": self.version})
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != "/api/regenerate":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length))

        cut_n      = int(body.get("cut_n", 1))
        prompt     = body.get("prompt", "").strip()
        mode       = body.get("mode", "image")
        model      = body.get("model", "nano_banana_2" if mode == "image" else "kling3_0_turbo")
        duration   = int(body.get("duration", 5))
        resolution = body.get("resolution", "2k" if mode == "image" else "1080p")

        if not prompt:
            self._send_json(400, {"error": "prompt이 비어 있습니다"})
            return

        vd = self.vdir()
        try:
            if mode == "image":
                url = regen_image(prompt, model, resolution=resolution)
                outpath = vd / "assets" / "images" / f"cut_{cut_n:02d}.png"
                urllib.request.urlretrieve(url, outpath)
                b64 = base64.b64encode(outpath.read_bytes()).decode()
                self._send_json(200, {
                    "ok": True, "cut_n": cut_n, "mode": "image",
                    "data_uri": f"data:image/png;base64,{b64}",
                    "source_url": url,
                })
            else:
                url = regen_video(prompt, model, duration=duration, resolution=resolution)
                outdir = vd / "assets" / "videos"
                outdir.mkdir(exist_ok=True)
                outpath = outdir / f"cut_{cut_n:02d}.mp4"
                urllib.request.urlretrieve(url, outpath)
                self._send_json(200, {
                    "ok": True, "cut_n": cut_n, "mode": "video",
                    "video_url": f"/api/videos/cut_{cut_n:02d}.mp4",
                    "source_url": url,
                })
        except Exception as e:
            self._send_json(500, {"error": str(e)})


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Higgsfield Review Server")
    ap.add_argument("--project", default="VELVET_NOIR")
    ap.add_argument("--version", default="v20260626")
    ap.add_argument("--port",    type=int, default=7800)
    args = ap.parse_args()

    ReviewHandler.project = args.project
    ReviewHandler.version = args.version

    server = HTTPServer(("localhost", args.port), ReviewHandler)
    url = f"http://localhost:{args.port}"
    print(f"\n  ▐ VELVET NOIR Review Server")
    print(f"  Project : {args.project} / {args.version}")
    print(f"  URL     : {url}")
    print(f"  Stop    : Ctrl+C\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
