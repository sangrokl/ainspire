#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Higgsfield Interactive Review Server
Usage: python3 system_v2/_review_server.py [--project VELVET_NOIR] [--version v20260626] [--port 7800]
Then open: http://localhost:7800

Auto-injection per request:
  1. 규칙0[A] mandatory prefix (angle/backlight/negative-fill rules)
  2. IMG_ENHANCE constant (cinematic photoreal + ARRI grain)
  3. [first frame] scene context from scenario.md
  4. --image <ref> : face ref (character cuts) / bottle ref (product cuts) / logo ref (logo cuts)
"""
import argparse, base64, json, mimetypes, os, re, subprocess
import threading, urllib.request, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Private-Network": "true",
}

# ── 규칙0[A] — MANDATORY IMAGE PREFIX ────────────────────────────────────────
RULE0A = (
    "MANDATORY IMAGE PREFIX — apply without exception: "
    "ZERO front-facing, ZERO eye-level. Subject NEVER looks into the lens. "
    "Use ONLY DUTCH-ANGLE / HIGH-ANGLE / LOW-ANGLE framing — pick per scene; "
    "off-center rule-of-thirds; telephoto shallow-DOF (demai) with clear 3-layer FG/MG/BG depth. "
    "Hard warm BACKLIGHT / rim-light from behind tracing the subject silhouette. "
    "BLACK NEGATIVE FILL on the shadow side — deep controlled shadow, LOW-KEY only, NEVER high-key."
)

# ── IMG_ENHANCE — cinematic quality constant ──────────────────────────────────
IMG_ENHANCE = (
    "CINEMATIC PHOTOREAL (append to every image prompt): "
    "Heightened photoreal realism with ENHANCED FACIAL DETAIL "
    "(lifelike skin micro-texture, visible pores, subsurface scattering, sharp eye catchlights). "
    "Real frame from a premium TV commercial — never CGI or illustration. "
    "Ultra-shallow demai depth of field, razor-thin focus plane, creamy bokeh. "
    "BACKLIGHT MANDATORY. NEGATIVE FILL MANDATORY. CRUSHED BLACKS in shadow regions. "
    "Heavy ARRI + anamorphic filmic grain. LOW-KEY luxurious grade."
)

# ── character description (NOIR) ──────────────────────────────────────────────
NOIR_DESC = (
    "CHARACTER — NOIR (주인공 여성): same face as the attached reference image. "
    "Dark hair, deep red lips, pale skin, intense gaze. "
    "Elegant, mysterious, luxury perfume commercial protagonist. "
    "Face NEVER front-facing, NEVER looking into the lens. "
    "MALE CHARACTER (2nd figure when present): face NEVER shown — "
    "back-of-head, shoulder silhouette, or hands only, always out-of-focus."
)

# ── Cut → reference image mapping ────────────────────────────────────────────
# bottle_cuts: product/bottle is the PRIMARY subject
BOTTLE_CUTS = {8, 25, 26, 27, 28}
# logo_cuts: logo wordmark is the PRIMARY subject
LOGO_CUTS   = {29, 30}
# all other cuts default to face ref


def _ref_paths(vd: Path, cut_n: int, use_face: bool = True,
               use_product: bool = True, use_logo: bool = True):
    """Return list of local ref paths to inject via --image flags."""
    ref = vd / "assets" / "ref"
    paths = []
    if cut_n in LOGO_CUTS:
        if use_logo:
            p = ref / "logo" / "logo_A_serif_wordmark.png"
            if p.exists(): paths.append(str(p))
        # logo cuts also get bottle ref for cut 30 (bottle+logo)
        if cut_n == 30 and use_product:
            p = ref / "product" / "ref_bottle_v2.png"
            if p.exists(): paths.append(str(p))
    elif cut_n in BOTTLE_CUTS:
        if use_product:
            p = ref / "product" / "ref_bottle_v2.png"
            if p.exists(): paths.append(str(p))
    else:
        if use_face:
            p = ref / "main_character" / "ref_face_v3.png"
            if p.exists(): paths.append(str(p))
    return paths


# ── scenario.md parser ────────────────────────────────────────────────────────
_scenario_cache: dict = {}

def parse_scenario(vd: Path) -> dict:
    """Parse scenario.md → {cut_n: {'first_frame': ..., 'shot': ..., 'sound': ...}}"""
    cache_key = str(vd)
    if cache_key in _scenario_cache:
        return _scenario_cache[cache_key]

    md = vd / "assets" / "md" / "scenario.md"
    if not md.exists():
        return {}

    txt = md.read_text(encoding="utf-8")
    cuts = {}
    for m in re.finditer(r'## Cut (\d+)\n(.*?)(?=\n## Cut \d+|\Z)', txt, re.DOTALL):
        n = int(m.group(1))
        body = m.group(2)
        cut = {}
        for field in ("shot", "first frame", "video prompt", "sound"):
            fm = re.search(rf'\[{re.escape(field)}\]:\s*(.+?)(?=\n\[|\Z)', body, re.DOTALL)
            if fm:
                cut[field.replace(" ", "_")] = fm.group(1).strip()
        cuts[n] = cut

    _scenario_cache[cache_key] = cuts
    return cuts


VIDEO_AUDIO = (
    "AUDIO: NO background music, NO score, NO BGM. "
    "Diegetic SFX ONLY — ambient room tone, natural sound, foley. "
    "Silence is preferred over any music."
)

def build_full_prompt(user_prompt: str, cut_n: int, vd: Path,
                      mode: str = "image") -> str:
    """Assemble: RULE0A + IMG_ENHANCE + NOIR desc + scene context + user revision."""
    scenario = parse_scenario(vd)
    scene    = scenario.get(cut_n, {})
    shot         = scene.get("shot", "")
    first_frame  = scene.get("first_frame", "")
    video_prompt = scene.get("video_prompt", "")

    parts = [RULE0A]

    if mode == "video":
        parts.append(VIDEO_AUDIO)
        if cut_n not in LOGO_CUTS and cut_n not in BOTTLE_CUTS:
            parts.append(NOIR_DESC)
        if shot:
            parts.append(f"SHOT TYPE: {shot}")
        if video_prompt:
            parts.append(f"ORIGINAL VIDEO PROMPT: {video_prompt}")
    else:
        parts.append(IMG_ENHANCE)
        if cut_n not in LOGO_CUTS and cut_n not in BOTTLE_CUTS:
            parts.append(NOIR_DESC)
        if shot:
            parts.append(f"SHOT TYPE: {shot}")
        if first_frame:
            parts.append(f"SCENE CONTEXT (original first frame): {first_frame}")

    parts.append(f"REVISION REQUEST: {user_prompt}")
    return "\n\n".join(parts)


# ── Version-safe file naming ─────────────────────────────────────────────────

def _next_version(folder: Path, cut_n: int, ext: str) -> Path:
    """Return next version path: cut_01_v1.png, cut_01_v2.png, …
    The original cut_01.png (from initial generation) is kept as-is.
    Revisions start from v1.
    """
    folder.mkdir(parents=True, exist_ok=True)
    v = 1
    while True:
        p = folder / f"cut_{cut_n:02d}_v{v}{ext}"
        if not p.exists():
            return p
        v += 1


# ── CLI runners ───────────────────────────────────────────────────────────────

def _run_cli(cmd, timeout=1200):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    raw = result.stdout.strip()
    if result.returncode != 0 and not raw:
        raise RuntimeError(result.stderr or "CLI returned no output")
    matches = re.findall(r'\{[\s\S]+\}', raw)
    if not matches:
        raise RuntimeError(f"No JSON in CLI output:\n{raw}\n{result.stderr}")
    return json.loads(matches[-1])


def _extract_url(data):
    if isinstance(data, dict):
        for k in ("result_url", "rawUrl", "url", "videoUrl", "imageUrl", "video_url", "image_url"):
            if k in data and isinstance(data[k], str) and data[k].startswith("http"):
                return data[k]
        for v in data.values():
            r = _extract_url(v)
            if r: return r
    elif isinstance(data, list):
        for item in data:
            r = _extract_url(item)
            if r: return r
    return None


def regen_image(prompt, model, resolution="2k", aspect_ratio="16:9", ref_paths=None):
    cmd = [
        "higgsfield", "generate", "create", model,
        "--prompt", prompt,
        "--aspect_ratio", aspect_ratio,
        "--resolution", resolution,
        "--wait", "--wait-timeout", "10m", "--wait-interval", "3s",
        "--json",
    ]
    for rp in (ref_paths or []):
        cmd += ["--image", rp]
    data = _run_cli(cmd, timeout=700)
    url  = _extract_url(data)
    if not url:
        raise RuntimeError(f"No URL in CLI response: {json.dumps(data)[:400]}")
    return url


def regen_video(prompt, model, duration=3, resolution="1080p", aspect_ratio="16:9", ref_paths=None):
    cmd = [
        "higgsfield", "generate", "create", model,
        "--prompt", prompt,
        "--aspect_ratio", aspect_ratio,
        "--duration", str(duration),
        "--resolution", resolution,
        "--wait", "--wait-timeout", "20m", "--wait-interval", "5s",
        "--json",
    ]
    for rp in (ref_paths or []):
        cmd += ["--image", rp]
    data = _run_cli(cmd, timeout=1300)
    url  = _extract_url(data)
    if not url:
        raise RuntimeError(f"No URL in CLI response: {json.dumps(data)[:400]}")
    return url


# ── HTTP Handler ──────────────────────────────────────────────────────────────

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
        try:
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_file(self, path):
        path = Path(path)
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            return
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        size = path.stat().st_size
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", size)
        self.send_header("Cache-Control", "no-cache")
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()
        try:
            with open(path, "rb") as f:
                while chunk := f.read(65536):
                    self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in CORS.items():
            self.send_header(k, v)
        self.end_headers()

    def do_HEAD(self):
        """Support HEAD for checkVideos() JS function."""
        p  = self.path.split("?")[0]
        vd = self.vdir()
        if p.startswith("/api/videos/"):
            fp = vd / "assets" / "videos" / p[len("/api/videos/"):]
            if fp.exists():
                self.send_response(200)
                self.send_header("Content-Length", fp.stat().st_size)
                for k, v in CORS.items():
                    self.send_header(k, v)
                self.end_headers()
            else:
                self.send_response(404)
                for k, v in CORS.items():
                    self.send_header(k, v)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        p  = self.path.split("?")[0]
        vd = self.vdir()

        if p in ("/", "/index.html"):
            self._send_file(vd / "preview" / f"storyboard_{self.project}_30cut_{self.version}.html")
        elif p.startswith("/api/images/"):
            self._send_file(vd / "assets" / "images" / p[len("/api/images/"):])
        elif p.startswith("/api/videos/"):
            self._send_file(vd / "assets" / "videos" / p[len("/api/videos/"):])
        elif p == "/api/status":
            self._send_json(200, {"ok": True, "project": self.project, "version": self.version})
        elif p == "/api/scene":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            n  = int(qs.get("n", [1])[0])
            sc = parse_scenario(vd).get(n, {})
            self._send_json(200, sc)
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
        user_prompt = body.get("prompt", "").strip()
        mode        = body.get("mode", "image")
        model       = body.get("model", "nano_banana_2" if mode == "image" else "kling3_0_turbo")
        duration    = int(body.get("duration", 3))
        resolution  = body.get("resolution", "2k" if mode == "image" else "1080p")
        use_face    = body.get("use_face", True)
        use_product = body.get("use_product", True)
        use_logo    = body.get("use_logo", True)

        if not user_prompt:
            self._send_json(400, {"error": "prompt이 비어 있습니다"})
            return

        vd = self.vdir()

        # Build enriched prompt
        full_prompt = build_full_prompt(user_prompt, cut_n, vd, mode=mode)
        ref_paths   = _ref_paths(vd, cut_n, use_face=use_face,
                                 use_product=use_product, use_logo=use_logo)

        # Log what's being injected
        inj = ["규칙0[A]", "IMG_ENHANCE"]
        if cut_n not in LOGO_CUTS and cut_n not in BOTTLE_CUTS:
            inj.append("NOIR_DESC")
        inj.append("씬컨텍스트")
        if ref_paths:
            inj.append(f"ref:{Path(ref_paths[0]).name}")
        print(f"  CUT {cut_n:02d} | 주입: {', '.join(inj)}")
        print(f"  모델: {model} | 해상도: {resolution}" +
              (f" | {duration}s" if mode == "video" else ""))

        try:
            if mode == "image":
                url = regen_image(full_prompt, model, resolution=resolution,
                                  ref_paths=ref_paths)
                img_dir  = vd / "assets" / "images"
                outpath  = _next_version(img_dir, cut_n, ".png")
                urllib.request.urlretrieve(url, outpath)
                b64 = base64.b64encode(outpath.read_bytes()).decode()
                print(f"  저장: {outpath.name}")
                self._send_json(200, {
                    "ok": True, "cut_n": cut_n, "mode": "image",
                    "filename": outpath.name,
                    "data_uri": f"data:image/png;base64,{b64}",
                    "source_url": url,
                    "injected": inj,
                })
            else:
                url = regen_video(full_prompt, model, duration=duration,
                                  resolution=resolution, ref_paths=ref_paths)
                vid_dir  = vd / "assets" / "videos"
                vid_dir.mkdir(exist_ok=True)
                outpath  = _next_version(vid_dir, cut_n, ".mp4")
                urllib.request.urlretrieve(url, outpath)
                print(f"  저장: {outpath.name}")
                self._send_json(200, {
                    "ok": True, "cut_n": cut_n, "mode": "video",
                    "filename": outpath.name,
                    "video_url": f"/api/videos/{outpath.name}",
                    "source_url": url,
                    "injected": inj,
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

    # Pre-warm scenario cache
    vd = ROOT / "projects" / args.project / args.version
    sc = parse_scenario(vd)
    print(f"\n  ▐ VELVET NOIR Review Server  (auto-injection ON)")
    print(f"  Project  : {args.project} / {args.version}")
    print(f"  Scenario : {len(sc)} cuts loaded from scenario.md")
    print(f"  Inject   : 규칙0[A] + IMG_ENHANCE + 씬컨텍스트 + ref이미지")
    print(f"  URL      : http://localhost:{args.port}")
    print(f"  Stop     : Ctrl+C\n")

    server = ThreadingHTTPServer(("localhost", args.port), ReviewHandler)
    threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{args.port}")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
