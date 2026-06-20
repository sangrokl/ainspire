# -*- coding: utf-8 -*-
import io, os, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "tether", "v20260620_v2")
RAW_DIR = os.path.join(VERSION_DIR, "images")
OUTFILE = "storyboard_TETHER_30cut_v20260620_v2.html"
ACCENT = "#caa46a"
TITLE = "TETHER · 스마트워치 — 30컷 스토리보드 v2"
SUB = ("30컷 · 16:9 · nano_banana_2/soul_2 img2img(re-derived 레퍼런스 ref_face_v2 고정). "
       "v1 대비 얼굴 레퍼런스를 cut_05 기준으로 재추출(soul_2)하고, 전 컷에 LOOK OVERRIDE 적용 — "
       "구도(앵글·배치·뎁스)는 승인된 스토리보드 시트를 따르되 레퍼런스 이미지의 조명은 무시하고 로우키·웜 백라이트 림으로 재조명. "
       "애플식 일상 감정 내러티브 '관계·연결' — 떨어져 있는 두 사람이 하루 종일 작은 연결로 이어지다 재회. "
       "그레이드: AWAY/HOME-early(1막) → WARM(2막) → HOME-reunion(3막) → FIN(피날레). "
       "정면·아이레벨 배제. 로고는 후반 합성.")

CUTS = [
    {"n": 1, "act": "1막", "scene": "AWAY — 낯선 호텔방, 새벽 블루 톤, 협탁 위 시계", "role": "배경 등장"},
    {"n": 2, "act": "1막", "scene": "HOME — 빈 침대 옆자리에 놓인 손, 아침 햇살", "role": "없음"},
    {"n": 3, "act": "1막", "scene": "AWAY — 출근 준비 중 멈춰진 사진이 떠 있는 시계화면을 잠깐 봄", "role": "약한 감정 등장"},
    {"n": 4, "act": "1막", "scene": "HOME — 혼자 커피 내리는 손, 머그 두 개 중 하나만 씀", "role": "없음"},
    {"n": 5, "act": "1막", "scene": "AWAY — 지하철 창 반사, 도시 풍경 블러", "role": "없음"},
    {"n": 6, "act": "1막", "scene": "HOME — 창가에 비친 실루엣, 기다리는 기운", "role": "없음"},
    {"n": 7, "act": "1막", "scene": "AWAY — 업무 중 습관적으로 손목 내려보지만 화면은 꺼져있음", "role": "없음(결핍 강조)"},
    {"n": 8, "act": "1막", "scene": "HOME — 저녁빛 사그라들며 시계를 탁자에 내려놓음", "role": "없음"},
    {"n": 9, "act": "2막 ★", "scene": "AWAY — 시계가 부드러운 햅틱 펄스, 손가락으로 탭 화답", "role": "결정적 순간 #1"},
    {"n": 10, "act": "2막", "scene": "HOME(수정) — 탑다운, 파트너 손목이 펄스를 받음, 골든아워", "role": "연동 반응"},
    {"n": 11, "act": "2막", "scene": "매크로 — 시계화면 추상 하트펄스 애니메이션", "role": "제품 클로즈업"},
    {"n": 12, "act": "2막", "scene": "HOME — 시계 화면으로 사진 전송(텍스트 없음)", "role": "연동"},
    {"n": 13, "act": "2막", "scene": "AWAY — 회의 중 손목 살짝 보고 미소", "role": "연동"},
    {"n": 14, "act": "2막", "scene": "HOME — 블라인드 사이 골든아워, 화면 쓸어보는 손", "role": "연동"},
    {"n": 15, "act": "2막", "scene": "AWAY — 저녁 거리, 소매 아래 시계, 네온 반사", "role": "배경 등장"},
    {"n": 16, "act": "2막", "scene": "HOME — 혼자 요리하다 카운터 위 시계 한 번 울림", "role": "연동"},
    {"n": 17, "act": "2막 ★", "scene": "AWAY(수정) — 익스트림 와이드·더치틸트, '귀환' 암시 알림에 기대감", "role": "결정적 순간 #2"},
    {"n": 18, "act": "2막", "scene": "HOME(수정) — 하이앵글, 파트너 손목에 알림이 비치며 희망", "role": "연동"},
    {"n": 19, "act": "3막", "scene": "AWAY — 짐 챙기며 마지막으로 시계 한 번 봄, 단호한 표정", "role": "배경"},
    {"n": 20, "act": "3막", "scene": "이동 — 기차/차량 도착, 도시 불빛 스트릭 모션블러", "role": "없음"},
    {"n": 21, "act": "3막", "scene": "HOME — 문 쪽을 보는 기다림의 정점", "role": "없음"},
    {"n": 22, "act": "3막", "scene": "문턱 — 실루엣 도착, 골든 백라이트 쏟아짐", "role": "없음"},
    {"n": 23, "act": "3막 ★", "scene": "포옹(수정) — 맞닿은 두 손목, 두 시계 나란히, 얼굴 풀샷 없음", "role": "결정적 순간 #3"},
    {"n": 24, "act": "3막", "scene": "HOME — 함께 있는 두 사람, 따뜻한 빛이 채움", "role": "정서적 동행"},
    {"n": 25, "act": "피날레", "scene": "매크로 — 다이얼 디테일, 로우키", "role": "제품 히어로"},
    {"n": 26, "act": "피날레", "scene": "매크로 — 스트랩 소재 질감", "role": "제품 히어로"},
    {"n": 27, "act": "피날레", "scene": "뷰티샷 — 다크 받침대 위 시계, 림라이트 실루엣", "role": "제품 히어로"},
    {"n": 28, "act": "피날레", "scene": "라이프스타일 — 따뜻한 우드 위 손목시계, 골든 글로우", "role": "제품 히어로"},
    {"n": 29, "act": "피날레", "scene": "브랜드 — 화면에 브랜드 마크 모션, 다크 배경", "role": "브랜드 모먼트"},
    {"n": 30, "act": "피날레", "scene": "최종 히어로 — 풀 프로덕트샷, 여백(태그라인용)", "role": "제품 히어로"},
]


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
        raw_path = os.path.join(RAW_DIR, f"cut_{c['n']:02d}.png")
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
