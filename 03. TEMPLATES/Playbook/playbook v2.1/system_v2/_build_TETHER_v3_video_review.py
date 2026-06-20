# -*- coding: utf-8 -*-
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "tether", "v20260620_v3")
OUTFILE = "video_review_TETHER_30cut_v20260620_v3.html"
ACCENT = "#caa46a"
TITLE = "TETHER · 스마트워치 — 30컷 영상 리뷰 (GATE 12)"
SUB = ("30컷 · 4초 · 1080p · 16:9 · seedance_2_0 (start_image=확정 컷, 컷별 카메라 무브먼트 배정). "
       "오디오는 디제틱 SFX만(No BGM, 규칙0[B]). 비디오는 용량 때문에 base64 임베드 대신 상대경로 참조 "
       "— 이 HTML과 videos/seedance/ 폴더를 같은 위치에 유지할 것.")

CUTS = [
    {"n": 1, "act": "1막", "scene": "AWAY — 호텔방 새벽, 슬로우 푸시인", "move": "슬로우 푸시인"},
    {"n": 2, "act": "1막", "scene": "HOME — 빈 침대 옆자리, 젠틀 핸드헬드", "move": "젠틀 핸드헬드"},
    {"n": 3, "act": "1막", "scene": "AWAY — 시계화면 사진, 푸시인", "move": "푸시인"},
    {"n": 4, "act": "1막", "scene": "HOME — 커피 내리는 손, 아크/오빗", "move": "아크/오빗"},
    {"n": 5, "act": "1막", "scene": "AWAY — 지하철 반사, 핸드헬드", "move": "핸드헬드"},
    {"n": 6, "act": "1막", "scene": "HOME — 창가 실루엣, 슬로우 푸시인", "move": "슬로우 푸시인"},
    {"n": 7, "act": "1막", "scene": "AWAY — 꺼진 시계화면, 틸트업", "move": "틸트업"},
    {"n": 8, "act": "1막", "scene": "HOME — 저녁 탁자, 크레인 풀업", "move": "크레인 풀업(슬로우)"},
    {"n": 9, "act": "2막 ★", "scene": "AWAY — 햅틱 펄스 탭, 크래시줌", "move": "크래시줌"},
    {"n": 10, "act": "2막", "scene": "HOME — 탑다운 수신 손목, 탑다운 푸시인", "move": "탑다운 푸시인"},
    {"n": 11, "act": "2막", "scene": "매크로 — 하트펄스 애니메이션, 매크로 플런지", "move": "매크로 플런지"},
    {"n": 12, "act": "2막", "scene": "HOME — 사진 전송, 아크/오빗", "move": "아크/오빗"},
    {"n": 13, "act": "2막", "scene": "AWAY — 오피스 손목 미소, 핸드헬드", "move": "핸드헬드"},
    {"n": 14, "act": "2막", "scene": "HOME — 화면 스와이프, 푸시인", "move": "푸시인"},
    {"n": 15, "act": "2막", "scene": "AWAY — 야간 거리 네온, 트래킹 핸드헬드", "move": "트래킹 핸드헬드"},
    {"n": 16, "act": "2막", "scene": "HOME — 요리 중 알림, 아크/오빗", "move": "아크/오빗"},
    {"n": 17, "act": "2막 ★", "scene": "AWAY — 익스트림 와이드 귀환 알림, 와이드 크레인", "move": "와이드 크레인"},
    {"n": 18, "act": "2막", "scene": "HOME — 하이앵글 알림, 오버헤드 푸시", "move": "오버헤드 푸시"},
    {"n": 19, "act": "3막", "scene": "AWAY — 짐 챙기는 마지막 시선, 달리인", "move": "달리인"},
    {"n": 20, "act": "3막", "scene": "이동 — 기차 도착, 다이내믹 트래킹", "move": "다이내믹 트래킹"},
    {"n": 21, "act": "3막", "scene": "HOME — 문 쪽 기다림, 푸시인", "move": "푸시인"},
    {"n": 22, "act": "3막", "scene": "문턱 — 실루엣 도착, 크래시줌", "move": "크래시줌"},
    {"n": 23, "act": "3막 ★", "scene": "포옹 — 두 손목, 슬로우 매크로 푸시인", "move": "슬로우 매크로 푸시인"},
    {"n": 24, "act": "3막", "scene": "HOME — 함께 있는 두 사람, 슬로우 아크/오빗", "move": "슬로우 아크/오빗"},
    {"n": 25, "act": "피날레", "scene": "매크로 — 다이얼 디테일, 매크로 플런지", "move": "매크로 플런지"},
    {"n": 26, "act": "피날레", "scene": "매크로 — 스트랩 텍스처, 매크로 오빗", "move": "매크로 오빗"},
    {"n": 27, "act": "피날레", "scene": "뷰티샷 — 다크 받침대, 로봇암 스윕", "move": "로봇암 다이내믹 스윕"},
    {"n": 28, "act": "피날레", "scene": "라이프스타일 — 우드 위 시계, 달리/아크", "move": "달리/아크"},
    {"n": 29, "act": "피날레", "scene": "브랜드 모먼트 — 화면 글로우, 크래시줌", "move": "크래시줌"},
    {"n": 30, "act": "피날레", "scene": "최종 히어로 — 풀 프로덕트샷, 로봇암/크레인", "move": "로봇암 스윕/크레인"},
]


def main():
    cards = []
    for c in CUTS:
        rel_path = f"videos/seedance/cut_{c['n']:02d}.mp4"
        cards.append(f"""
      <div class="card">
        <video src="{rel_path}" autoplay muted loop playsinline></video>
        <div class="meta"><span class="cut" style="background:{ACCENT}">{c['n']:02d}</span><span class="tag">{c['act']}</span></div>
        <p class="cap">{c['scene']}</p>
        <p class="move">무브: {c['move']}</p>
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
  .card video{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover;background:#000}}
  .meta{{display:flex;align-items:center;gap:8px;padding:10px 12px 0}}
  .cut{{color:#0b0d12;font-weight:800;font-size:12px;padding:2px 9px;border-radius:6px}}
  .tag{{font-size:11px;color:#aeb6c8;font-weight:600;letter-spacing:-.01em}}
  .cap{{margin:7px 12px 2px;font-size:13px;color:#d3d9e6;line-height:1.45}}
  .move{{margin:0 12px 13px;font-size:11px;color:{ACCENT};font-weight:700}}
</style></head><body>
  <header><h1>{TITLE}</h1><p>{SUB}</p></header>
  <div class="grid">{''.join(cards)}</div>
</body></html>"""

    path = os.path.join(VERSION_DIR, OUTFILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", path, round(os.path.getsize(path) / 1024, 1), "KB")


if __name__ == "__main__":
    main()
