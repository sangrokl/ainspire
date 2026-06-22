# -*- coding: utf-8 -*-
import io, os, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "VOLT", "v20260622")
RAW_DIR = os.path.join(VERSION_DIR, "images")
OUTFILE = "storyboard_VOLT_30cut_v20260622_v2.html"
ACCENT = "#3ddc97"
TITLE = "VOLT · 에너지드링크 — 30컷 스토리보드 v1 (성취·도전 내러티브)"
SUB = ("30컷 · 16:9 · nano_banana_2 img2img(주인공·제품 레퍼런스 고정). "
       "애플식 일상 감정 내러티브 '성취·도전' — 새벽엔 마라톤을 준비하고 낮엔 일에 쫓기는 RAE가 "
       "결심→한계→돌파를 거쳐 결승선을 넘는다. "
       "그레이드: COLD(1막, 새벽 블루) → PUSH(2막, 고대비 앰버) → GOLD(3막·피날레, 골든아워). "
       "정면·아이레벨 배제, 로우키+웜 백라이트 림. BGM·내레이션·로고는 후반 합성.")

CUTS = [
    {"n": 1, "act": "1막", "scene": "새벽 4:58 알람 끄는 손 클로즈업", "role": "없음"},
    {"n": 2, "act": "1막", "scene": "눈 뜨는 ECU, 동공에 결승선 시계 어렴풋", "role": "없음"},
    {"n": 3, "act": "1막", "scene": "차가운 바닥에 발 내딛는 로우앵글", "role": "없음"},
    {"n": 4, "act": "1막", "scene": "밤샘 오피스, 유리벽 너머 도시 불빛", "role": "없음"},
    {"n": 5, "act": "1막", "scene": "노트북 불빛 속 결심이 스치는 얼굴", "role": "없음"},
    {"n": 6, "act": "1막", "scene": "복도에서 정장 위에 운동화 갈아신기", "role": "없음"},
    {"n": 7, "act": "1막", "scene": "새벽 텅 빈 거리로 나서는 와이드 로우앵글", "role": "없음"},
    {"n": 8, "act": "1막", "scene": "식탁 위 VOLT 캔, 새벽빛이 스치다", "role": "제품 첫 등장"},
    {"n": 9, "act": "2막", "scene": "강변 트랙 새벽 러닝, 하이앵글", "role": "없음"},
    {"n": 10, "act": "2막", "scene": "땀에 젖은 옆얼굴 텔레포토 클로즈업", "role": "없음"},
    {"n": 11, "act": "2막", "scene": "다리 더치앵글, 물웅덩이 스플래시", "role": "없음"},
    {"n": 12, "act": "2막", "scene": "손목 러닝워치 인서트, 페이스 상승", "role": "없음"},
    {"n": 13, "act": "2막", "scene": "벤치에서 무너지는 와이드샷", "role": "없음"},
    {"n": 14, "act": "2막 ★", "scene": "벤치 위 VOLT 캔 쥐는 손 클로즈업", "role": "결정적 순간 #1"},
    {"n": 15, "act": "2막 ★", "scene": "첫 모금 OTS 숏", "role": "결정적 순간 #1"},
    {"n": 16, "act": "2막 ★", "scene": "캔 스파크 마크 매크로 플레어", "role": "결정적 순간 #1"},
    {"n": 17, "act": "2막", "scene": "벤치에서 일어서는 로우앵글, 회복", "role": "없음"},
    {"n": 18, "act": "2막", "scene": "두번째 바람 — 아크샷 스프린트, 골드로 전환", "role": "없음"},
    {"n": 19, "act": "3막", "scene": "마라톤 출발 코랄, 신발끈 묶기", "role": "없음"},
    {"n": 20, "act": "3막", "scene": "출발선 하이앵글, 군중의 질주", "role": "없음"},
    {"n": 21, "act": "3막", "scene": "한계의 순간 — 더치앵글 클로즈업", "role": "없음"},
    {"n": 22, "act": "3막", "scene": "오르막에서 흔들리는 다리, 추월당함", "role": "없음"},
    {"n": 23, "act": "3막 ★", "scene": "급수대에서 VOLT 캔 받아 쥐기", "role": "결정적 순간 #2"},
    {"n": 24, "act": "3막 ★", "scene": "달리며 한 모금, 구름 사이 골든라이트", "role": "결정적 순간 #2"},
    {"n": 25, "act": "피날레", "scene": "다른 러너를 추월하는 로우앵글", "role": "없음"},
    {"n": 26, "act": "피날레", "scene": "피니시라인 통과, 두 팔 들어올림", "role": "없음"},
    {"n": 27, "act": "피날레", "scene": "환희의 미소 클로즈업", "role": "없음"},
    {"n": 28, "act": "피날레 ★", "scene": "황금빛 하늘 배경 제품 히어로샷", "role": "결정적 순간 #3"},
    {"n": 29, "act": "피날레 ★", "scene": "캔 스파크 마크 매크로 시머", "role": "결정적 순간 #3"},
    {"n": 30, "act": "피날레", "scene": "엔드카드 팩샷, 여백에 로고 자리", "role": "엔드카드"},
]


def find_raw(n):
    for ext in ("png", "jpeg", "jpg"):
        p = os.path.join(RAW_DIR, f"cut_{n:02d}_v2.{ext}")
        if os.path.exists(p):
            return p
    for ext in ("png", "jpeg", "jpg"):
        p = os.path.join(RAW_DIR, f"cut_{n:02d}.{ext}")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"cut_{n:02d} not found in {RAW_DIR}")


def datauri(path, width=760, quality=80):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    cards = []
    for c in CUTS:
        raw_path = find_raw(c["n"])
        uri = datauri(raw_path)
        role_html = f'<p class="role">{c["role"]}</p>' if c["role"] != "없음" else ""
        cards.append(f"""
      <div class="card">
        <img src="{uri}" alt="C{c['n']:02d}"/>
        <div class="meta"><span class="cut" style="background:{ACCENT}">{c['n']:02d}</span><span class="tag">{c['act']}</span></div>
        <p class="cap">{c['scene']}</p>
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
