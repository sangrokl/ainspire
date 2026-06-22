# -*- coding: utf-8 -*-
import io, os, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "energy-runner", "v20260621")
RAW_DIR = os.path.join(VERSION_DIR, "images")
OUTFILE = "storyboard_ENERGYRUNNER_30cut_v20260621.html"
ACCENT = "#ff5a2e"
TITLE = "ENERGY RUNNER · 에너지드링크 — 30컷 스토리보드"
SUB = ("30컷 · 16:9 · nano_banana_2/gpt_image_2 img2img(주인공·제품 레퍼런스 고정). "
       "애플식 일상 감정 내러티브 '성취·도전' — 매일 새벽 마라톤 완주를 향해 도전하는 아마추어 러너, "
       "작은 좌절을 이겨내고 결승선을 넘는다. "
       "그레이드: COLD(1막, 새벽 블루) → STRAIN(2막, 중성 그레이) → WARM(3막, 노을 골드) → FIN(피날레, 강렬 레드/오렌지). "
       "정면·아이레벨 배제, 로우키+웜 백라이트 림. 로고는 후반 합성.")

CUTS = [
    {"n": 1, "act": "1막", "scene": "알람 끄는 손, 어두운 방 다치앵글", "role": "없음"},
    {"n": 2, "act": "1막", "scene": "일어나 창밖 새벽빛 바라보는 옆모습", "role": "없음"},
    {"n": 3, "act": "1막", "scene": "운동화 끈 묶는 손 클로즈업", "role": "없음"},
    {"n": 4, "act": "1막", "scene": "현관문 열고 나서는 뒷모습", "role": "없음"},
    {"n": 5, "act": "1막", "scene": "텅 빈 새벽 거리 홀로 달리기 시작, 탑다운 뷰", "role": "없음"},
    {"n": 6, "act": "1막", "scene": "가쁜 숨, 입김 나는 옆얼굴 클로즈업", "role": "없음"},
    {"n": 7, "act": "1막", "scene": "손목 러닝 앱 화면 인서트(거리·페이스)", "role": "없음"},
    {"n": 8, "act": "1막", "scene": "저 멀리 결승선 게이트 실루엣 — 결심의 표정", "role": "없음"},
    {"n": 9, "act": "2막", "scene": "비 오는 새벽 훈련, 역경", "role": "없음"},
    {"n": 10, "act": "2막", "scene": "힘겨운 다리 근육 클로즈업, 더치앵글", "role": "없음"},
    {"n": 11, "act": "2막", "scene": "벤치에 지친 모습, 흐린 실루엣(코치) 다가옴", "role": "없음"},
    {"n": 12, "act": "2막 ★", "scene": "건네받는 캔 — 손 클로즈업, 차가운 캔 표면, 역광", "role": "결정적 순간 #1"},
    {"n": 13, "act": "2막", "scene": "캔 따는 손 + 가로등 백라이트", "role": "제품 등장"},
    {"n": 14, "act": "2막", "scene": "한 모금, 고개 젖히는 옆모습 — 깨어나는 느낌", "role": "제품 등장"},
    {"n": 15, "act": "2막", "scene": "다시 속도 붙는 다리, 모션블러", "role": "없음"},
    {"n": 16, "act": "2막", "scene": "야경 거리 매치컷, 하이앵글", "role": "없음"},
    {"n": 17, "act": "2막", "scene": "비 그치고 해 뜨는 하늘, 실루엣", "role": "없음"},
    {"n": 18, "act": "3막", "scene": "트랙에서 동료(얼굴 안 보임)와 인터벌 훈련 투샷", "role": "없음"},
    {"n": 19, "act": "3막", "scene": "대회 날 새벽 출발선, 군중 속 옆모습", "role": "없음"},
    {"n": 20, "act": "3막", "scene": "출발 총성, 뛰쳐나가는 발 클로즈업", "role": "없음"},
    {"n": 21, "act": "3막", "scene": "코스 중간 힘든 표정 — 한계의 순간", "role": "없음"},
    {"n": 22, "act": "3막 ★", "scene": "한계의 순간 보급소 캔을 움켜쥐는 손, 네거티브 필", "role": "결정적 순간 #2"},
    {"n": 23, "act": "3막", "scene": "다시 힘내는 다리, 다이내믹 로우앵글", "role": "없음"},
    {"n": 24, "act": "3막", "scene": "결승선 가까워지는 관중 실루엣 매치컷", "role": "없음"},
    {"n": 25, "act": "피날레", "scene": "결승선 통과, 두 팔 들어올림, 하이앵글", "role": "없음"},
    {"n": 26, "act": "피날레", "scene": "환희의 표정 클로즈업, 땀+미소", "role": "없음"},
    {"n": 27, "act": "피날레 ★", "scene": "결승선 직후 캔 들어올리는 피날레, 역광 실루엣", "role": "결정적 순간 #3"},
    {"n": 28, "act": "피날레", "scene": "제품 히어로샷 — 캔 단독 매크로, 스파크 모티프 강조", "role": "제품 히어로"},
    {"n": 29, "act": "피날레", "scene": "캔 표면에 비치는 결승선 조명 반사 인서트", "role": "제품 히어로"},
    {"n": 30, "act": "피날레", "scene": "브랜드 마무리 컷 — 캔+로고 여백, 강렬 그레이드", "role": "브랜드 모먼트"},
]


def find_raw(n):
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
