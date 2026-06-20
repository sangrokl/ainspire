# -*- coding: utf-8 -*-
import io, os, base64
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "tether", "v20260620_v3")
IMG_DIR = os.path.join(VERSION_DIR, "images")
LOGO_PATH = os.path.join(VERSION_DIR, "images", "logo", "logo_v3_transparent.png")
OUTFILE = "storyboard_TETHER_FINAL_v20260620_v3.html"
ACCENT = "#caa46a"
TITLE = "TETHER"
TAGLINE = "Stay close, wherever you are."

OVERVIEW = [
    ("컨셉", "애플식 일상 감정 내러티브 '관계, 연결' - 떨어져 있는 두 사람이 하루 종일 작은 연결로 이어지다 재회"),
    ("레퍼런스", "Apple Watch <911>형 리얼 스토리 문법, 노을과 블라인드 인물 레시피"),
    ("타깃, 톤", "친근하고 따뜻한 분위기 - 밝은 텅스텐 조명, 생활감 + 로우키 시네마틱"),
    ("막 구조", "1막 도입(8컷, 결핍) - 2막 전개(10컷, 작은 연결 3회) - 3막 해소(6컷, 재회) - 피날레(6컷, 제품 히어로)"),
    ("컬러 서사", "AWAY(차가운 블루) - WARM(앰버골드 상승) - HOME-reunion(골든아워) - FIN(로우키 럭셔리)"),
    ("촬영 문법", "정면, 아이레벨 배제. 더치, 로우, 하이, 탑다운 앵글. 데마이 얕은 심도. 웜 백라이트 림. 네거티브 필"),
    ("일관성", "주인공 얼굴 레퍼런스와 제품 레퍼런스를 전 컷에 고정 (nano_banana_2)"),
    ("제품 역할", "결정적 순간 3개 (햅틱 펄스, 귀환 알림, 재회 포옹) + 피날레 히어로샷"),
    ("기술 스펙", "이미지: nano_banana_2, 2K, 16:9 / 영상: seedance_2_0, 4초, 1080p, 16:9 / VO: ElevenLabs Brian / BGM: Suno (트렌디 힙, 102 BPM, 사용자 생성)"),
]

VO_LINES = {
    1: ("00:00", "Some distances aren't measured in miles."),
    5: ("00:04", "They're measured in moments you almost shared."),
    9: ("00:08", "TETHER closes that gap - one quiet pulse at a time."),
    17: ("00:16", "A tap. A heartbeat. A reason to come home sooner."),
    23: ("00:22", "Because the best connections don't wait for words."),
    27: ("00:26", "TETHER. Stay close, wherever you are."),
}

CUTS = [
    {"n": 1, "act": "1막", "scene": "AWAY - 낯선 호텔방, 새벽 블루 톤, 협탁 위 시계", "shot": "슬로우 푸시인"},
    {"n": 2, "act": "1막", "scene": "HOME - 빈 침대 옆자리에 놓인 손, 아침 햇살", "shot": "젠틀 핸드헬드"},
    {"n": 3, "act": "1막", "scene": "AWAY - 출근 준비 중 시계화면 속 사진을 봄", "shot": "푸시인"},
    {"n": 4, "act": "1막", "scene": "HOME - 혼자 커피 내리는 손, 머그 두 개", "shot": "아크/오빗"},
    {"n": 5, "act": "1막", "scene": "AWAY - 지하철 창 반사, 도시 풍경 블러", "shot": "핸드헬드"},
    {"n": 6, "act": "1막", "scene": "HOME - 창가에 비친 실루엣, 기다리는 기운", "shot": "슬로우 푸시인"},
    {"n": 7, "act": "1막", "scene": "AWAY - 습관적으로 손목을 보지만 화면은 꺼짐", "shot": "틸트업"},
    {"n": 8, "act": "1막", "scene": "HOME - 저녁빛 사그라들며 시계를 내려놓음", "shot": "크레인 풀업"},
    {"n": 9, "act": "2막 (결정적 순간 1)", "scene": "AWAY - 시계가 부드러운 햅틱 펄스, 손가락 탭", "shot": "크래시줌"},
    {"n": 10, "act": "2막", "scene": "HOME - 탑다운, 파트너 손목이 펄스를 받음", "shot": "탑다운 푸시인"},
    {"n": 11, "act": "2막", "scene": "매크로 - 시계화면 하트펄스 애니메이션", "shot": "매크로 플런지"},
    {"n": 12, "act": "2막", "scene": "HOME - 시계 화면으로 사진 전송", "shot": "아크/오빗"},
    {"n": 13, "act": "2막", "scene": "AWAY - 회의 중 손목 보고 미소", "shot": "핸드헬드"},
    {"n": 14, "act": "2막", "scene": "HOME - 골든아워, 화면 쓸어보는 손", "shot": "푸시인"},
    {"n": 15, "act": "2막", "scene": "AWAY - 저녁 거리, 네온 반사, 시계", "shot": "트래킹 핸드헬드"},
    {"n": 16, "act": "2막", "scene": "HOME - 혼자 요리하다 시계 한 번 울림", "shot": "아크/오빗"},
    {"n": 17, "act": "2막 (결정적 순간 2)", "scene": "AWAY - 익스트림 와이드, 귀환 암시 알림", "shot": "와이드 크레인"},
    {"n": 18, "act": "2막", "scene": "HOME - 하이앵글, 파트너 손목에 알림 비침", "shot": "오버헤드 푸시"},
    {"n": 19, "act": "3막", "scene": "AWAY - 짐 챙기며 마지막으로 시계를 봄", "shot": "달리인"},
    {"n": 20, "act": "3막", "scene": "이동 - 기차 도착, 도시 불빛 스트릭", "shot": "다이내믹 트래킹"},
    {"n": 21, "act": "3막", "scene": "HOME - 문 쪽을 보는 기다림의 정점", "shot": "푸시인"},
    {"n": 22, "act": "3막", "scene": "문턱 - 실루엣 도착, 골든 백라이트", "shot": "크래시줌"},
    {"n": 23, "act": "3막 (결정적 순간 3)", "scene": "포옹 - 맞닿은 두 손목, 두 시계 나란히", "shot": "슬로우 매크로 푸시인"},
    {"n": 24, "act": "3막", "scene": "HOME - 함께 있는 두 사람, 따뜻한 빛", "shot": "슬로우 아크/오빗"},
    {"n": 25, "act": "피날레", "scene": "매크로 - 다이얼 디테일, 로우키", "shot": "매크로 플런지"},
    {"n": 26, "act": "피날레", "scene": "매크로 - 스트랩 소재 질감", "shot": "매크로 오빗"},
    {"n": 27, "act": "피날레", "scene": "뷰티샷 - 다크 받침대 위 시계", "shot": "로봇암 스윕"},
    {"n": 28, "act": "피날레", "scene": "라이프스타일 - 우드 위 손목시계, 골든 글로우", "shot": "달리/아크"},
    {"n": 29, "act": "피날레", "scene": "브랜드 모먼트 - 화면 글로우, 다크 배경", "shot": "크래시줌"},
    {"n": 30, "act": "피날레", "scene": "최종 히어로 - 풀 프로덕트샷, 여백", "shot": "로봇암/크레인"},
]


def datauri(path, width=560, quality=80):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def logo_datauri(path):
    img = Image.open(path).convert("RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    overview_cards = "".join(
        f'<div class="ocard"><h4>{k}</h4><p>{v}</p></div>' for k, v in OVERVIEW
    )

    cut_cards = []
    for i, c in enumerate(CUTS):
        n = c["n"]
        raw_path = os.path.join(IMG_DIR, f"cut_{n:02d}.png")
        uri = datauri(raw_path)
        tc = f"00:{i:02d}"
        vo_html = ""
        if n in VO_LINES:
            _, line = VO_LINES[n]
            vo_html = f'<p class="vo">VO: &ldquo;{line}&rdquo;</p>'
        cut_cards.append(f"""
      <div class="card">
        <img src="{uri}" alt="C{n:02d}"/>
        <div class="meta"><span class="cut" style="background:{ACCENT}">{n:02d}</span><span class="tag">{c['act']}</span><span class="tc">{tc}</span></div>
        <p class="cap">{c['scene']}</p>
        <p class="shot">{c['shot']}</p>
        {vo_html}
      </div>""")

    logo_uri = logo_datauri(LOGO_PATH)

    vo_rows = "".join(f"<tr><td>{tc}</td><td>{line}</td></tr>" for tc, line in VO_LINES.values())

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><title>{TITLE} - FINAL Storyboard</title>
<style>
  :root{{color-scheme:dark}}*{{box-sizing:border-box}}
  body{{margin:0;background:#0b0d12;color:#e7eaf0;font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}}
  header{{padding:48px 32px 24px;display:flex;align-items:center;gap:20px;border-bottom:1px solid #1e2330}}
  header img{{height:48px}}
  header .htext h1{{margin:0;font-size:28px;letter-spacing:-.02em;color:{ACCENT}}}
  header .htext p{{margin:4px 0 0;color:#8b93a7;font-size:13px}}
  section{{padding:32px}}
  section h2{{font-size:16px;color:{ACCENT};margin:0 0 16px;letter-spacing:.02em;text-transform:uppercase}}
  .overview{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
  .ocard{{background:#12151c;border:1px solid #1e2330;border-radius:12px;padding:14px 16px}}
  .ocard h4{{margin:0 0 6px;font-size:12px;color:{ACCENT};text-transform:uppercase;letter-spacing:.03em}}
  .ocard p{{margin:0;font-size:13px;color:#d3d9e6;line-height:1.5}}
  .vo-block{{background:#12151c;border:1px solid #1e2330;border-radius:12px;padding:18px 20px}}
  .vo-block table{{width:100%;border-collapse:collapse;font-size:13px}}
  .vo-block td{{padding:6px 10px;border-bottom:1px solid #1e2330;color:#d3d9e6}}
  .vo-block td:first-child{{color:{ACCENT};font-weight:700;width:70px}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
  .card{{background:#12151c;border:1px solid #1e2330;border-radius:14px;overflow:hidden}}
  .card img{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}}
  .meta{{display:flex;align-items:center;gap:8px;padding:10px 12px 0}}
  .cut{{color:#0b0d12;font-weight:800;font-size:12px;padding:2px 9px;border-radius:6px}}
  .tag{{font-size:11px;color:#aeb6c8;font-weight:600}}
  .tc{{margin-left:auto;font-size:11px;color:#6b7280;font-family:monospace}}
  .cap{{margin:7px 12px 0;font-size:13px;color:#d3d9e6;line-height:1.4}}
  .shot{{margin:2px 12px 0;font-size:11px;color:#8b93a7}}
  .vo{{margin:6px 12px 13px;font-size:11px;color:{ACCENT};font-weight:700;font-style:italic}}
</style></head><body>
  <header><img src="{logo_uri}" alt="logo"/><div class="htext"><h1>{TITLE}</h1><p>{TAGLINE} - 30컷 최종 완성 스토리보드 (v20260620_v3)</p></div></header>
  <section><h2>기획안 개요</h2><div class="overview">{overview_cards}</div></section>
  <section><h2>내레이션 VO (영문, 30초, Brian 보이스 확정)</h2>
    <div class="vo-block"><table>
      {vo_rows}
    </table>
    <p style="margin:12px 0 0;font-size:11px;color:#6b7280">오디오: projects/tether/v20260620_v3/audio/vo/tether_brian.mp3 (A2 트랙). BGM(A1)은 Suno에서 사용자가 직접 생성한 mp3가 준비되면 조건부로 추가.</p>
    </div>
  </section>
  <section><h2>30컷 그리드 / 타임코드</h2><div class="grid">{''.join(cut_cards)}</div></section>
</body></html>"""

    path = os.path.join(VERSION_DIR, OUTFILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", path, round(os.path.getsize(path) / 1024 / 1024, 2), "MB")


if __name__ == "__main__":
    main()
