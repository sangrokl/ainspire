# -*- coding: utf-8 -*-
import io, os, json, base64, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "RISE", "v20260619_v2")
MANIFEST = os.path.join(VERSION_DIR, "images", "manifest.json")
RAW_DIR = os.path.join(VERSION_DIR, "images", "raw")
OUTFILE = "storyboard_RISE_30cut_v20260619_v2.html"
ACCENT = "#c9a24b"
TITLE = "RISE · 프리미엄 에너지드링크 — 30컷 스토리보드 v2"
SUB = ("30컷 · 16:9 · nano_banana_2 img2img. v1 대비 컷15·16·17·24·25·26 렌즈/앵글 다양화 재생성 "
       "(200mm f/2.8 망원 / 16mm 광각 / 익스트림 클로즈업 / 85mm 워룸즈아이 로우앵글 / 100mm 매크로 탑다운 / 24mm 극단 로우앵글). "
       "나머지 24컷은 v1 그대로. 애플식 일상 감정 내러티브 '회복·성장'. "
       "그레이드: AWAY(1막)→STRAIN(2막)→WARM(3막)→GOLDEN(피날레). 정면·아이레벨 배제. 로고는 후반 합성.")

os.makedirs(RAW_DIR, exist_ok=True)


def download(url, path):
    if os.path.exists(path):
        return
    subprocess.run(["curl", "-sL", "-o", path, url], check=True)


def datauri(path, width=760, quality=80):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        cuts = json.load(f)

    cards = []
    for c in cuts:
        raw_path = os.path.join(RAW_DIR, f"cut_{c['cut']:02d}.png")
        download(c["url"], raw_path)
        uri = datauri(raw_path)
        role = c["product_role"]
        role_html = f'<p class="role">{role}</p>' if role != "없음" else ""
        cards.append(f"""
      <div class="card">
        <img src="{uri}" alt="C{c['cut']:02d}"/>
        <div class="meta"><span class="cut" style="background:{ACCENT}">{c['cut']:02d}</span><span class="tag">{c['act']}</span></div>
        <p class="cap">{c['scene_kr']}</p>
        {role_html}
      </div>""")

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><title>{TITLE}</title>
<style>
  :root{{color-scheme:dark}}*{{box-sizing:border-box}}
  body{{margin:0;background:#0b0d12;color:#e7eaf0;font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}}
  header{{padding:40px 32px 8px}}
  header h1{{margin:0 0 6px;font-size:26px;letter-spacing:-.02em;color:{ACCENT}}}
  header p{{margin:0;color:#8b93a7;font-size:13px;line-height:1.6}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;padding:24px 32px 48px}}
  .card{{background:#12151c;border:1px solid #1e2330;border-radius:14px;overflow:hidden}}
  .card img{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}}
  .meta{{display:flex;align-items:center;gap:8px;padding:10px 12px 0}}
  .cut{{color:#0b0d12;font-weight:800;font-size:12px;padding:2px 9px;border-radius:6px}}
  .tag{{font-size:11px;color:#aeb6c8;font-weight:600;letter-spacing:-.01em}}
  .cap{{margin:7px 12px 2px;font-size:13px;color:#d3d9e6;line-height:1.45}}
  .role{{margin:0 12px 13px;font-size:11px;color:{ACCENT};font-weight:700}}
</style></head><body>
  <header><h1>{TITLE}</h1><p>{SUB}</p></header>
  <div class="grid">{''.join(cards)}</div>
</body></html>"""

    path = os.path.join(VERSION_DIR, OUTFILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", path, round(os.path.getsize(path) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    main()
