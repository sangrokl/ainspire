# -*- coding: utf-8 -*-
import io, base64, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def datauri(path, width=760, quality=82):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width); img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------- HALO ----------------
HALO_DIR = os.path.join(ROOT, r"projects\commercial\halo_watch\v2026-05-29_v10\images\storyboard")
HALO_OUT = os.path.join(ROOT, r"projects\commercial\halo_watch\v2026-05-29_v10\storyboard_HALO_FINAL_v2026-05-29.html")
HALO_ACCENT = "#39e0a0"
HALO_TITLE = "HALO · 스마트워치 — 완성 스토리보드"
HALO_TAG = "「몇 분을 가른 신호」 · 애플워치 '911' 리얼스토리 문법 · 30컷 · 4초/컷 · 16:9"
# (num, act, shot, scene)
HALO_CUTS = [
 ("01","起","초광각 항공","광활한 능선의 작은 트레일러너, 황혼"),
 ("02","起","로우앵글 ECU","바위 차는 트레일화+워치, 분투"),
 ("03","起","더치 ECU","옆얼굴 거친 숨·땀"),
 ("04","起","탑다운 매크로","[유용] 워치 페이스·심박·고도"),
 ("05","起","하이앵글 와이드","절벽 끝, 거대한 산, 빛이 진다"),
 ("06","起","도어 너머 달리인","집: 2인분 저녁 준비 실루엣, 기다림"),
 ("07","承","광각 더치 휩팬","미끄러지는 돌, 추락"),
 ("08","承","스팁 하이앵글","비탈에 쓰러진 그, 뒤틀린 다리"),
 ("09","承","로우앵글 ECU","깨진 폰·신호 없음"),
 ("10","承","익스트림 하이앵글","어두워지는 비탈의 작은 형체"),
 ("11","承","더치 ECU","통증·공포, 입김"),
 ("12","轉","더치 매크로","[유용] 낙상 감지 → 긴급 SOS 점등"),
 ("13","轉","로우앵글 ECU","[유용] SOS 연결, 어둠 속 그린루미=생명선"),
 ("14","轉","로우 틸트업","[유용] 손목 들어 위치·심박 전송"),
 ("15","轉","하이앵글 와이드","멀리 구조대 불빛 깨어남 (수정본)"),
 ("16","轉","로우앵글 ECU","[유용] 칠흑 속 워치=비콘"),
 ("17","轉","오버숄더 망원","비탈 오르는 헤드램프들"),
 ("18","轉","더치 ECU","첫 구조광이 얼굴을 쓸고 — 희망"),
 ("19","結","로우앵글 역광","구조대(페이스리스) 도달, 플레어"),
 ("20","結","ECU 데마이","어깨 부축·포일 담요, 안전"),
 ("21","結","로봇암 와이드","산악 야간 헬기 구조 (수정본)"),
 ("22","結","뒤/하이앵글","사랑하는 사람(페이스리스) 포옹"),
 ("23","結","더치 매크로","실내 맞잡은 손+워치, 안도 (수정본)"),
 ("24","結","뒤/하이 와이드","무사 귀가, 자막 여백"),
 ("25","FIN","제품 아크","빛줄기 속 티타늄 다이브 워치"),
 ("26","FIN","로우앵글 매크로","그린루미 빛고리 HALO 모티프"),
 ("27","FIN","더치 ECU","티타늄 케이스 디테일"),
 ("28","FIN","탑다운 매크로","SOS·심박 글로우"),
 ("29","FIN","로우앵글 와이드","별 아래 워치"),
 ("30","FIN","로우앵글 역광 엔딩","새벽 능선, 손목 든 워치 (로고)"),
]
HALO_VO = {  # primary narration (A · Brian) mapped to beat-start cuts
 "01":"He went up alone, the way he liked it.",
 "07":"A loose rock, a hard fall — no way down, and no signal to call for help.",
 "12":"But his watch felt the fall.",
 "13":"It reached for help, and told them exactly where he was.",
 "17":"That night, the mountain didn't keep him.",
 "25":"HALO. It watches, so someone always knows.",
}
HALO_PLAN = [
 ("컨셉","「몇 분을 가른 신호」 — 고독한 산악 트레일 사고에서 워치의 낙상감지·긴급 SOS·비콘이 생명을 잇는 실화형 30초."),
 ("레퍼런스","Apple Watch 〈911〉 캠페인(실제 구조 사례). 제품을 설명하지 않고 '삶의 순간'으로 가치를 증명."),
 ("타깃·톤","아웃도어·프리미엄 / 시네마틱 로우키, 긴장 → 안도. 정면·아이레벨 배제."),
 ("4막 구조","起 고독한 모험(01–06) · 承 사고·고립(07–11) · 轉 워치 작동·구조 호출(12–18) · 結 구조·재회(19–24) · FIN 제품/브랜드(25–30)."),
 ("컬러 서사","ADV 황혼산 → CRISIS 차가운 블루 → RESCUE 구조광 → HOME 골든 → FIN 나이트."),
 ("촬영 문법","로우/하이/더치·다이내믹 광각·데마이 얕은심도, 매치컷·트랜지션 연결, '움직이는 샷의 키프레임'."),
 ("일관성","시그니처 트레일 룩·동일 얼굴 락 / 2번째 인물·구조대 완전 페이스리스(실루엣·손·헤드램프)."),
 ("워치 역할","낙상 감지 · 긴급 SOS · 위치·심박 전송 · 어둠 속 비콘 — 결정적 순간에만 담백하게."),
 ("스펙","30컷 · 1792×1008 16:9 · gpt-image-2 img2img / 영상 Seedance 2.0 4초·1080p / 로고·자막 후반 합성."),
]
HALO_VO_NOTE = ("내레이션: 다큐 스타일 · 차분한 미국 남성. 아래는 A안(Brian, Deep·Comforting). "
 "대안 B안(Eric, Smooth·Trustworthy) / C안(Roger, Laid-Back·Resonant) — audio/vo/halo_vo_*.mp3.")

# ---------------- AETHER ----------------
AE_DIR = os.path.join(ROOT, r"projects\commercial\aether_energy\v2026-05-29_v3\images\storyboard")
AE_OUT = os.path.join(ROOT, r"projects\commercial\storyboard_AETHER_FINAL_v2026-05-29.html")
AE_ACCENT = "#3aa0ff"
AE_TITLE = "AETHER · 에너지드링크 — 완성 스토리보드"
AE_TAG = "3막 변신 서사 · 무채색 일상 → 일렉트릭 블루 코스믹 충전 → 색의 복귀 · 30컷 · 16:9"
AE_CUTS = [
 ("01","ACT1","ECU 데마이","형광등 반사된 지친 얼굴, 무거운 오후"),
 ("02","ACT1","망원 하이앵글","회색 오피스, 책상에 늘어진 그"),
 ("03","ACT1","ECU","꾸벅 떨어지는 눈꺼풀, 풀린 초점"),
 ("04","ACT1","ECU","식은 커피+멈춘 듯한 시계"),
 ("05","ACT1","더치 화면","빈 문서 커서만 깜빡, 멈춘 진도바"),
 ("06","ACT1","역광 실루엣","블라인드 역광에 늘어진 어깨"),
 ("07","ACT1","로우앵글","무겁게 일어서는 다리, 권태의 기동"),
 ("08","ACT1","망원압축","끝없는 회색 복도, 작게 걷는 그"),
 ("09","ACT2","매크로 인서트","자판기서 성에 낀 캔 꺼냄 — 제품 등장"),
 ("10","ACT2","매크로 더치","캔 쥔 손, 회색 속 캔만 채도"),
 ("11","ACT2","ECU","탭 따는 손가락, 빛이 변함 — 트리거"),
 ("12","ACT2","로우앵글 CU","한 모금, 목울대 블루 림라이트 점화"),
 ("13","ACT2","ECU 눈","동공 점화+배경 균열 빛"),
 ("14","ACT3","더치 광각","복도가 유리처럼 갈라지며 빛 분출"),
 ("15","ACT3","로우앵글 광각","무중력 부상, 집기 공중 부유"),
 ("16","ACT3","제품 아트","블루 액체 크라운 스플래시"),
 ("17","ACT3","망원압축","부유 사물 가르며 질주·비행"),
 ("18","ACT3","유리 인서트","빛 파편에 분열된 역동 실루엣"),
 ("19","ACT3","제품 아트","캔 휘감는 에너지 빛 리본"),
 ("20","ACT3","로우앵글","빛 기둥 박차고 도약"),
 ("21","ACT3","ECU 데마이","블루 반사된 강렬한 눈빛"),
 ("22","ACT3","제품 아트","얼음·물 스플래시 캔 히어로"),
 ("23","ACT3","망원압축 더치","코스믹 블루 공간 실루엣 절정"),
 ("24","ACT3","제품 아트","개봉 증기+블루 라이트 버스트"),
 ("25","ACT3","더치 광각","빛 소용돌이 현실로 수렴 — 귀환"),
 ("26","복귀","ECU","다시 또렷해진 눈, 채도 복귀"),
 ("27","복귀","로우앵글 3/4 백","자리로 복귀, 키보드 위 손"),
 ("28","복귀","망원압축","막혔던 화면 단숨에 채움, 가벼워진 공간"),
 ("29","복귀","매크로","캔 히어로, 역광 글로우+결로"),
 ("30","복귀","로우키 히어로","창가 역광 실루엣, 캔 든 그 (로고)"),
]
AE_VO = {  # primary narration (A · Adam, tough baritone)
 "01":"There are days the world tries to drain you. Days the gray wins.",
 "09":"Then you take the spark back.",
 "12":"One pull of AETHER — and the current hits.",
 "14":"Electric. Alive. Unstoppable.",
 "27":"AETHER. Charge your storm.",
}
AE_PLAN = [
 ("컨셉","무채색 번아웃 일상 → 음료 한 모금으로 일렉트릭 블루 코스믹 에너지가 충전 → 색이 돌아온 자신감으로 복귀하는 3막 변신 서사."),
 ("타깃·톤","에너지·각성 / 프리미엄 블루 판타지, 고대비. 제품을 매 컷 들이대지 않고 '변신'으로 위력을 보여줌."),
 ("3막 구조","ACT1 일상의 벽·그레이(01–08) · ACT2 트리거·포털(09–13) · ACT3 코스믹 위력(14–25) · 복귀·충전완료(26–30)."),
 ("컬러 서사","무채색 그레이 → 일렉트릭 블루 코스믹(채도 폭발) → 채도 복귀. 캔만 회색 속에서 먼저 색을 얻음."),
 ("촬영 문법","ECU 데마이·역광 실루엣·거울/에너지 예술 인서트·매치컷, 정면·아이레벨·풀샷 배제, 블랙 프로미스트, 로우키 실사."),
 ("제품 역할","트리거(포털)·에너지 시각화로 서사에 녹임. 히어로 제품샷은 ACT3·피날레에 집중."),
 ("스펙","30컷 · 1792×1008 16:9 · gpt-image-2 img2img / 로고 후반 합성."),
]
AE_VO_NOTE = ("내레이션: 터프한 미국 남성 중저음. 아래는 A안(Adam, Dominant·Firm). "
 "대안 B안(Brian, Deep·Resonant) / C안(Callum, Husky) — audio/vo/aether_vo_*.mp3.")

CSS = """
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:#0b0d12;color:#e7eaf0;font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}
header{padding:44px 36px 10px}
header .kick{font-size:12px;letter-spacing:.18em;color:#6f7891;text-transform:uppercase;margin-bottom:8px}
header h1{margin:0 0 8px;font-size:32px;letter-spacing:-.02em;color:__ACCENT__}
header .tag{margin:0;color:#aeb6c8;font-size:14px;line-height:1.6}
section{padding:12px 36px}
h2{font-size:13px;letter-spacing:.14em;color:__ACCENT__;text-transform:uppercase;margin:22px 0 12px;border-top:1px solid #1e2330;padding-top:18px}
.plan{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.pcard{background:#12151c;border:1px solid #1e2330;border-radius:12px;padding:13px 15px}
.pcard .k{font-size:11px;font-weight:800;color:__ACCENT__;letter-spacing:.04em;margin-bottom:5px}
.pcard .v{font-size:13px;color:#cfd6e4;line-height:1.55}
.vo{background:#101a16;border:1px solid #203a30;border-radius:12px;padding:16px 18px}
.vo .note{font-size:12px;color:#8b93a7;margin:0 0 12px;line-height:1.55}
.vo .line{display:flex;gap:12px;padding:6px 0;border-bottom:1px dashed #1c2a24;font-size:14px;line-height:1.5}
.vo .line:last-child{border-bottom:0}
.vo .tc{color:__ACCENT__;font-weight:700;font-size:12px;min-width:54px;font-variant-numeric:tabular-nums}
.vo .tx{color:#e7eaf0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:8px 36px 56px}
.card{background:#12151c;border:1px solid #1e2330;border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.card img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}
.meta{display:flex;align-items:center;gap:8px;padding:10px 12px 0;flex-wrap:wrap}
.cut{color:#0b0d12;font-weight:800;font-size:12px;padding:2px 9px;border-radius:6px;background:__ACCENT__}
.act{font-size:10px;font-weight:800;color:__ACCENT__;border:1px solid __ACCENT__;border-radius:5px;padding:1px 6px}
.tc2{font-size:11px;color:#6f7891;font-variant-numeric:tabular-nums}
.tag{font-size:11px;color:#aeb6c8;font-weight:600}
.cap{margin:7px 12px 4px;font-size:13px;color:#d3d9e6;line-height:1.45}
.void{margin:0 12px 13px;font-size:12px;color:#9fe6c6;line-height:1.45;font-style:italic}
.void b{color:__ACCENT__;font-style:normal}
.aevoid{color:#9fc8ff !important}
"""

def page(title, kick, tag, plan, vo_note, vo_map, cuts, dir_, accent, outfile, vo_class=""):
    css = CSS.replace("__ACCENT__", accent)
    # narration lines block (from vo_map in cut order)
    vo_lines = []
    for num, _, _, _ in cuts:
        if num in vo_map:
            sec = int(num) - 1
            vo_lines.append(f'<div class="line"><span class="tc">00:{sec:02d}</span><span class="tx">{vo_map[num]}</span></div>')
    plan_html = "".join(f'<div class="pcard"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in plan)
    cards = []
    for num, act, shot, scene in cuts:
        uri = datauri(os.path.join(dir_, ("halo_c" if "HALO" in title else "aether_c") + num + ".png"))
        sec = int(num) - 1
        vo = f'<p class="void {vo_class}">🎙 <b>VO</b> "{vo_map[num]}"</p>' if num in vo_map else ""
        cards.append(f"""
      <div class="card">
        <img src="{uri}" alt="C{num}"/>
        <div class="meta"><span class="cut">C{num}</span><span class="act">{act}</span><span class="tc2">00:{sec:02d}</span><span class="tag">{shot}</span></div>
        <p class="cap">{scene}</p>{vo}
      </div>""")
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><title>{title}</title>
<style>{css}</style></head><body>
  <header><div class="kick">{kick}</div><h1>{title}</h1><p class="tag">{tag}</p></header>
  <section><h2>기획안 개요</h2><div class="plan">{plan_html}</div></section>
  <section><h2>내레이션 (영문 VO · 30초)</h2><div class="vo"><p class="note">{vo_note}</p>{''.join(vo_lines)}</div></section>
  <section><h2>스토리보드 30컷</h2></section>
  <div class="grid">{''.join(cards)}</div>
</body></html>"""
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", outfile, round(os.path.getsize(outfile)/1024/1024, 2), "MB")

page(HALO_TITLE, "HALO SMARTWATCH · COMMERCIAL", HALO_TAG, HALO_PLAN, HALO_VO_NOTE, HALO_VO, HALO_CUTS, HALO_DIR, HALO_ACCENT, HALO_OUT)
page(AE_TITLE, "AETHER ENERGY · COMMERCIAL", AE_TAG, AE_PLAN, AE_VO_NOTE, AE_VO, AE_CUTS, AE_DIR, AE_ACCENT, AE_OUT, vo_class="aevoid")
