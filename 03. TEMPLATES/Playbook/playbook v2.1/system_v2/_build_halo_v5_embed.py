# -*- coding: utf-8 -*-
import io, base64, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HL_DIR = os.path.join(ROOT, r"projects\halo_watch\v2026-05-29_v5\images\storyboard")
OUT_DIR = os.path.join(ROOT, r"projects\halo_watch\v2026-05-29_v5")
OUTFILE = "storyboard_HALO_30cut_v2026-05-29_v5.html"
ACCENT = "#39e0a0"
TITLE = "HALO · 스마트워치 — 30컷 스토리보드 v5 (거리 · 연결 내러티브)"
SUB = ("30컷 v5 - 1792x1008 16:9 - gpt-image-2 img2img. 애플식 일상 내러티브 '거리(Distance)'. "
       "타지로 떠난 한 남자의 며칠 - 집/사랑하는 사람과 떨어져 있는 그리움 → 하루 종일 이어지는 작은 연결 → 거리를 좁혀 재회. "
       "워치는 기능 데모가 아니라 '두 사람을 잇는 보이지 않는 끈'(안부·하트비트 탭·함께 닫은 활동링·귀가 안내)으로만 등장, "
       "제품은 피날레에서만 히어로. 2번째 인물은 실루엣·뒷모습·손·사진·화면으로 처리. "
       "데마이 망원 + 역광 실루엣 + 거울/유리 인서트 + 매치컷 + 컬러콘트라스트 극대화 + 배경 미술/소품 디테일. 정면·아이레벨 배제. 로고는 후반 합성.")

def datauri(path, width=760, quality=80):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# (file, seq#, act-tag, scene, watch-thread)
HALO = [
 ("halo_c01","01","[AWAY] 망원 뒷모습","새벽 타지 호텔 통창, 작게 선 그 - 거리감","—"),
 ("halo_c02","02","[AWAY] ECU","차가운 유리에 얹은 손, 발밑 도시 보케","—"),
 ("halo_c03","03","[AWAY→온기] 데마이","협탁 워치에 집에서 온 아침 안부 글로우","안부 메시지"),
 ("halo_c04","04","[온기] ECU 옆얼굴","메시지 읽는 옅은 미소 - 그리움","—"),
 ("halo_c05","05","[온기] 정물","가족/집 사진(아웃포커스), 식은 커피","—"),
 ("halo_c06","06","[AWAY] 망원압축","낯선 도심 군중 속 홀로 걷는 그","—"),
 ("halo_c07","07","[온기] ECU","가방 속 아이의 그림·쪽지 - 따뜻한 컬러","—"),
 ("halo_c08","08","[온기] 데마이","로비, 집에서 온 하트비트 탭이 손목에 도착","하트비트 탭"),
 ("halo_c09","09","[온기] 유리 인서트","먼 도시+따뜻한 집이 한 프레임 반사","—"),
 ("halo_c10","10","[HOME] 실루엣","집 창가, 그(녀)도 그를 그리워함","—"),
 ("halo_c11","11","[HOME] 데마이","집의 작은 손·다른 손목, 활동링 닫기","활동링 닫기"),
 ("halo_c12","12","[온기] ECU","거리 너머 함께 닫은 활동링 - 공동의 승리","공유 활동링"),
 ("halo_c13","13","[온기] 망원","옥상 발코니, 골든아워 집 쪽 응시 - 결심","—"),
 ("halo_c14","14","[온기] ECU 데마이","워치로 '곧 끝나' 짧은 메시지 - 친밀한 끈","메시지"),
 ("halo_c15","15","[온기] 인서트","황혼 도시불빛 보케, 난간의 작은 실루엣","—"),
 ("halo_c16","16","[HOME] 정물","현관 작은 신발, 켜둔 불, 기다리는 실루엣","—"),
 ("halo_c17","17","[AWAY] 데마이","밤 호텔방, 캐리어 닫으며 사진 마지막에","—"),
 ("halo_c18","18","[AWAY] 매크로","떠나며 어둠 속 워치 글로우, 창의 빗방울","매치컷셋업"),
 ("halo_c19","19","연결 인서트","빗줄기 기차창→따뜻한 집 창불빛 디졸브(무인)","—"),
 ("halo_c20","20","[온기→HOME] 망원","밤기차 흐르는 도시→교외 불빛, 그의 반사","—"),
 ("halo_c21","21","[HOME] ECU","워치 '곧 도착' 안내 - 설렘, 온기 지배","도착 안내"),
 ("halo_c22","22","[HOME] 역광","밤거리로 내려 집 향해 서두름, 입김·림라이트","—"),
 ("halo_c23","23","[HOME] 재회","현관문 열림, 쏟아지는 따뜻한 빛, 달려와 안기는 실루엣","—"),
 ("halo_c24","24","[HOME] ECU","재회, 맞닿은 두 손목·손 - 거리=0, 끈의 완성","함께"),
 # ---- finale ----
 ("halo_c25","25","[FIN] 제품 아트","따뜻한 빛줄기 속 워치 히어로","—"),
 ("halo_c26","26","[FIN] 매크로","그린루미 빛고리 HALO 모티프 - 잇는 원","—"),
 ("halo_c27","27","[FIN] ECU","티타늄 케이스 따뜻한 반사 디테일","—"),
 ("halo_c28","28","[FIN] 매크로","페이스의 하트비트/활동링 - '연결' 감성","—"),
 ("halo_c29","29","[FIN] 유리 인서트","따뜻한 집 창에 워치 레이어","—"),
 ("halo_c30","30","[FIN] 로우키 엔딩","따뜻한 현관 실루엣, 손목 든 워치 글로우","엔딩(로고 후반)"),
]

def main():
    cards = []
    for fn, num, tag, cap, conn in HALO:
        uri = datauri(os.path.join(HL_DIR, fn + ".png"))
        cards.append(f"""
      <div class="card">
        <img src="{uri}" alt="C{num}"/>
        <div class="meta"><span class="cut" style="background:{ACCENT}">{num}</span><span class="tag">{tag}</span></div>
        <p class="cap">{cap}</p>
        <p class="conn">{conn}</p>
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
  .conn{{margin:0 12px 13px;font-size:11px;color:#6f7891}}
</style></head><body>
  <header><h1>{TITLE}</h1><p>{SUB}</p></header>
  <div class="grid">{''.join(cards)}</div>
</body></html>"""
    path = os.path.join(OUT_DIR, OUTFILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", path, round(os.path.getsize(path)/1024/1024,2), "MB")

if __name__ == "__main__":
    main()
