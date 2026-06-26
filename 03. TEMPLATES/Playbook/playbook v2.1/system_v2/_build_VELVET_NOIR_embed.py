# -*- coding: utf-8 -*-
import io, os, base64
from PIL import Image

ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_DIR = os.path.join(ROOT, "projects", "VELVET_NOIR", "v20260626")
RAW_DIR     = os.path.join(VERSION_DIR, "assets", "images")
PREVIEW_DIR = os.path.join(VERSION_DIR, "preview")
OUTFILE     = "storyboard_VELVET_NOIR_30cut_v20260626.html"
ACCENT      = "#c9a227"
RED         = "#a01020"
TITLE       = "VELVET NOIR · 향수 광고 — 30컷 스토리보드"
SUB         = ("30컷 · 16:9 · nano_banana_2 img2img(주인공·향수병 ref 고정). "
               "미스터리 러버 + 유혹의 여신 하이브리드 — 하루(아침→밤) 타임라인. "
               "그레이드: MORNING(쿨 블루그레이) → TENSION(딥 카마인+앰버) → "
               "CONNECT(웜 골드+피콕레드) → FINALE(퓨어 블랙+크리스털). "
               "정면·아이레벨 배제, 로우키 + 웜 백라이트 림. 남성 2번 인물 얼굴 절대 노출 금지.")

CUTS = [
    {"n":  1, "act": "1막·MORNING",  "scene": "ECU 눈 반사 — 새벽 창문빛이 홍채에 맺힘",               "role": ""},
    {"n":  2, "act": "1막·MORNING",  "scene": "로우앵글 매크로 — 손이 향수병에 뻗는 다치앵글",         "role": ""},
    {"n":  3, "act": "1막·MORNING",  "scene": "다치앵글 CU — 목·쇄골 역광 실루엣, 머리카락 흘러내림",  "role": ""},
    {"n":  4, "act": "1막·MORNING",  "scene": "ECU 손목 미스트 — 향수 분사 슬로모션",                  "role": "★ 결정적 순간 #1"},
    {"n":  5, "act": "1막·MORNING",  "scene": "하이앵글 OTS 거울 — 반사 속 딥레드 입술만",            "role": ""},
    {"n":  6, "act": "1막·MORNING",  "scene": "다치앵글 ECU 딥레드 입술 — 매치컷 준비",                "role": ""},
    {"n":  7, "act": "1막·MORNING",  "scene": "로우앵글 — NOIR 전신 실루엣, 창가 새벽빛 역광",         "role": ""},
    {"n":  8, "act": "1막·MORNING",  "scene": "익스트림 매크로 — 크리스털 병이 아침빛 프리즘 분산",    "role": ""},
    {"n":  9, "act": "2막·TENSION",  "scene": "탑다운 버즈아이뷰 — 로비 입장, 군중 보케 방사형",       "role": ""},
    {"n": 10, "act": "2막·TENSION",  "scene": "플로어레벨 로우앵글 — 힐이 대리석 타격, 루비 반사",     "role": ""},
    {"n": 11, "act": "2막·TENSION",  "scene": "망원 압축 — 군중 속 NOIR만 샤프, 다치앵글",             "role": ""},
    {"n": 12, "act": "2막·TENSION",  "scene": "ECU 손 — 크림슨 벨벳 커튼을 스치는 슬로모션",          "role": ""},
    {"n": 13, "act": "2막·TENSION",  "scene": "하이앵글 다치 — NOIR가 빛 문턱에 멈춤, 고개 기울임",   "role": ""},
    {"n": 14, "act": "2막·TENSION",  "scene": "로우앵글 — 남성 실루엣(등·어깨만) 회전 시작",           "role": ""},
    {"n": 15, "act": "2막·TENSION",  "scene": "익스트림 망원 — NOIR 샤프 우측, 남성 블러 좌측",        "role": ""},
    {"n": 16, "act": "2막·TENSION",  "scene": "ECU 남성 목 뒤 → 매치컷 NOIR의 알듯한 미소",            "role": "★ 결정적 순간 #2"},
    {"n": 17, "act": "2막·TENSION",  "scene": "다치앵글 CU 쇄골 — 향수 바른 피부서 앰버 빛 번짐",     "role": ""},
    {"n": 18, "act": "2막·TENSION",  "scene": "매크로 — 남성 손이 뻗다 멈춤, 절제",                    "role": ""},
    {"n": 19, "act": "3막·CONNECT",  "scene": "OTS 라운지 — NOIR 측면 시선, 골드 스탠드 램프만",        "role": ""},
    {"n": 20, "act": "3막·CONNECT",  "scene": "망원 CU 손 — 크리스털 잔 들어올림, 반지 스파클",         "role": ""},
    {"n": 21, "act": "3막·CONNECT",  "scene": "다치앵글 — 어두운 유리 패널 속 두 사람 반사",            "role": ""},
    {"n": 22, "act": "3막·CONNECT",  "scene": "ECU — 두 손이 1mm 거리, 결정의 순간",                    "role": ""},
    {"n": 23, "act": "3막·CONNECT",  "scene": "로우앵글 트래킹 — NOIR가 멀어짐, 드레스 끝 끌림",       "role": ""},
    {"n": 24, "act": "3막·CONNECT",  "scene": "ECU 반얼굴 — 깊은 그림자+골드 슬리버, 아는 미소",       "role": ""},
    {"n": 25, "act": "피날레·FINALE", "scene": "매크로 — 크리스털 병이 퓨어 블랙 속 천천히 회전",       "role": ""},
    {"n": 26, "act": "피날레·FINALE", "scene": "익스트림 매크로 — 보석 하나, 내부 스펙트럼",             "role": ""},
    {"n": 27, "act": "피날레·FINALE", "scene": "풀 히어로샷 — 보석 장식 크리스털 병, 퓨어 블랙",        "role": "★ 결정적 순간 #3"},
    {"n": 28, "act": "피날레·FINALE", "scene": "매크로 슬로모 — 펌프 분사 미스트 네뷸러",                "role": ""},
    {"n": 29, "act": "피날레·FINALE", "scene": "로우앵글 타이포 — 골드 세리프 워드마크 인",              "role": ""},
    {"n": 30, "act": "피날레·FINALE", "scene": "최종 — 병+워드마크 컴포지션, 보석 캐치라이트, 페이드",   "role": "브랜드 모먼트"},
]

IMG_MODELS = [
    ("nano_banana_2",    "Nano Banana Pro"),
    ("nano_banana_flash","Nano Banana 2"),
    ("flux_2",           "FLUX.2"),
    ("seedream_v4_5",    "Seedream 4.5"),
    ("gpt_image_2",      "GPT Image 2"),
    ("flux_kontext",     "Flux Kontext"),
]

VID_MODELS = [
    ("kling3_0_turbo",        "Kling 3.0 Turbo"),
    ("kling3_0",              "Kling v3.0"),
    ("seedance_2_0",          "Seedance 2.0"),
    ("seedance_2_0_mini",     "Seedance 2.0 Mini"),
    ("cinematic_studio_3_0",  "Cinematic Studio 3.0"),
    ("veo3",                  "Google Veo 3"),
    ("veo3_1",                "Google Veo 3.1"),
]


def find_raw(n):
    for ext in ("png", "jpeg", "jpg"):
        p = os.path.join(RAW_DIR, f"cut_{n:02d}.{ext}")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"cut_{n:02d} not found in {RAW_DIR}")


def datauri(path, width=760, quality=82):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        h = int(img.height * width / img.width)
        img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build_img_options():
    return "".join(
        f'<option value="{v}"{" selected" if i==0 else ""}>{n}</option>'
        for i, (v, n) in enumerate(IMG_MODELS)
    )


def build_vid_options():
    return "".join(
        f'<option value="{v}"{" selected" if i==0 else ""}>{n}</option>'
        for i, (v, n) in enumerate(VID_MODELS)
    )


# ── JavaScript (kept as raw string so {{ }} in JS are preserved) ─────────────
JS = r"""
// SERVER: relative path when served via http, absolute when opened as file://
const IS_FILE = window.location.protocol === 'file:';
const SERVER  = IS_FILE ? 'http://localhost:7800' : '';
const cuts = JSON.parse(document.getElementById('cuts-data').textContent);

// Show file:// warning banner
if (IS_FILE) {
  const b = document.getElementById('file-banner');
  b.style.display = 'block';
  document.getElementById('srv-open-link').href = 'http://localhost:7800';
}

// ── server ping (AbortController for broad browser compat) ───────────────────
async function pingServer() {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 2000);
  try {
    const r = await fetch(SERVER + '/api/status', {
      signal: ctrl.signal,
      mode: 'cors',
      cache: 'no-store',
    });
    clearTimeout(timer);
    return r.ok;
  } catch {
    clearTimeout(timer);
    return false;
  }
}

async function updateServerBadge() {
  const badge = document.getElementById('srv-badge');
  const ok = await pingServer();
  badge.textContent = ok ? '● 서버 연결됨' : '○ 서버 오프라인';
  badge.className   = 'srv-badge ' + (ok ? 'ok' : 'off');
  if (!ok && IS_FILE) {
    badge.title = '파일로 열었습니다 — 서버를 먼저 실행하세요: python3 system_v2/_review_server.py';
  } else {
    badge.title = ok ? '리뷰 서버 실행 중' : '서버 오프라인: python3 system_v2/_review_server.py';
  }
}
setInterval(updateServerBadge, 8000);
updateServerBadge();

// ── panel state ───────────────────────────────────────────────────────────────
let selectedCut = null;

function selectCard(n) {
  document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
  const card = document.querySelector(`.card[data-n="${n}"]`);
  if (!card) return;
  card.classList.add('selected');
  selectedCut = n;

  const cut = cuts.find(c => c.n === n);
  document.getElementById('panel-cut-n').textContent  = `CUT ${String(n).padStart(2,'0')}`;
  document.getElementById('panel-cut-act').textContent = cut ? cut.act : '';
  document.getElementById('panel-cut-scene').textContent = cut ? cut.scene : '';
  document.getElementById('prompt-input').value = '';
  document.getElementById('prompt-input').placeholder = '수정 요청사항을 입력하세요…';
  clearStatus();

  const panel = document.getElementById('review-panel');
  panel.classList.add('open');
  document.getElementById('prompt-input').focus();
}

function closePanel() {
  document.getElementById('review-panel').classList.remove('open');
  document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
  selectedCut = null;
}

// ── mode toggle ───────────────────────────────────────────────────────────────
function setMode(mode) {
  document.getElementById('mode-image').classList.toggle('active', mode === 'image');
  document.getElementById('mode-video').classList.toggle('active', mode === 'video');
  document.getElementById('video-opts').style.display = mode === 'video' ? 'block' : 'none';
  document.getElementById('img-res-row').style.display = mode === 'image' ? 'flex' : 'none';
  document.getElementById('img-model-wrap').style.display = mode === 'image' ? 'block' : 'none';
  document.getElementById('vid-model-wrap').style.display = mode === 'video' ? 'block' : 'none';
}
setMode('image');

document.getElementById('mode-image').addEventListener('click', () => setMode('image'));
document.getElementById('mode-video').addEventListener('click', () => setMode('video'));

// ── duration / quality pills ──────────────────────────────────────────────────
document.querySelectorAll('.pill-dur').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.pill-dur').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
  });
});
document.querySelectorAll('.pill-vq').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.pill-vq').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
  });
});
document.querySelectorAll('.pill-iq').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.pill-iq').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
  });
});

// ── status helpers ────────────────────────────────────────────────────────────
function setStatus(msg, type) {
  const el = document.getElementById('gen-status');
  el.textContent = msg;
  el.className   = 'gen-status ' + (type || '');
}
function clearStatus() { setStatus(''); }

// ── submit ────────────────────────────────────────────────────────────────────
async function submitRegen() {
  if (!selectedCut) return;

  const prompt = document.getElementById('prompt-input').value.trim();
  if (!prompt) { setStatus('수정 요청사항을 입력하세요', 'err'); return; }

  const online = await pingServer();
  if (!online) {
    setStatus('서버 오프라인 — python3 system_v2/_review_server.py 실행 후 재시도', 'err');
    return;
  }

  const mode = document.getElementById('mode-image').classList.contains('active') ? 'image' : 'video';
  const model = mode === 'image'
    ? document.getElementById('img-model-sel').value
    : document.getElementById('vid-model-sel').value;
  const duration   = parseInt(document.querySelector('.pill-dur.active')?.dataset.val || '5');
  const vidQuality = document.querySelector('.pill-vq.active')?.dataset.val || '1080p';
  const imgQuality = document.querySelector('.pill-iq.active')?.dataset.val || '2k';
  const resolution = mode === 'image' ? imgQuality : vidQuality;

  const btn = document.getElementById('gen-btn');
  btn.disabled = true;
  setStatus('⏳ 생성 중… (수 분 소요)', 'loading');

  try {
    const res = await fetch(SERVER + '/api/regenerate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cut_n: selectedCut, prompt, mode, model, duration, resolution }),
      mode: 'cors',
    });
    const data = await res.json();

    if (!res.ok || !data.ok) {
      setStatus('오류: ' + (data.error || '서버 응답 실패'), 'err');
      return;
    }

    // Update card thumbnail
    const card = document.querySelector(`.card[data-n="${selectedCut}"]`);
    const thumb = card.querySelector('.card-thumb');

    if (mode === 'image') {
      thumb.innerHTML = `<img src="${data.data_uri}" alt="C${selectedCut}"/>`;
      card.querySelector('.updated-badge')?.remove();
      const badge = document.createElement('span');
      badge.className = 'updated-badge';
      badge.textContent = '✓ 업데이트됨';
      card.querySelector('.meta').appendChild(badge);
      setStatus('✓ 이미지 업데이트 완료', 'ok');
    } else {
      thumb.innerHTML = `<video src="${data.video_url}" autoplay loop muted playsinline
        style="width:100%;display:block;aspect-ratio:16/9;object-fit:cover;"></video>`;
      card.querySelector('.updated-badge')?.remove();
      const badge = document.createElement('span');
      badge.className = 'updated-badge vid';
      badge.textContent = '▶ 영상 추가됨';
      card.querySelector('.meta').appendChild(badge);
      setStatus('✓ 영상 생성 완료', 'ok');
    }
  } catch (e) {
    setStatus('연결 오류: ' + e.message, 'err');
  } finally {
    btn.disabled = false;
  }
}

// Enter to submit (Shift+Enter = newline)
document.getElementById('prompt-input').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitRegen(); }
});
document.getElementById('gen-btn').addEventListener('click', submitRegen);
document.getElementById('panel-close').addEventListener('click', closePanel);

// Escape closes panel
document.addEventListener('keydown', e => { if (e.key === 'Escape') closePanel(); });
"""


def main():
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    # Build cards
    cuts_json = []
    cards_html = []
    for c in CUTS:
        raw_path = find_raw(c["n"])
        uri = datauri(raw_path)
        is_moment = c["role"].startswith("★")
        accent_c  = RED if is_moment else ACCENT
        border    = f"border:1px solid {RED};box-shadow:0 0 10px {RED}44;" if is_moment else "border:1px solid #1e2330;"
        role_html = f'<p class="role">{c["role"]}</p>' if c["role"] else ""
        cuts_json.append({"n": c["n"], "act": c["act"], "scene": c["scene"]})
        cards_html.append(f"""
      <div class="card" data-n="{c['n']}" style="{border}" onclick="selectCard({c['n']})">
        <div class="card-thumb"><img src="{uri}" alt="C{c['n']:02d}"/></div>
        <div class="meta">
          <span class="cut" style="background:{accent_c}">{c['n']:02d}</span>
          <span class="tag">{c['act']}</span>
        </div>
        <p class="cap">{c['scene']}</p>
        {role_html}
      </div>""")

    img_opts = build_img_options()
    vid_opts = build_vid_options()
    import json as _json
    cuts_json_str = _json.dumps(cuts_json, ensure_ascii=False)

    html = f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{TITLE}</title>
<style>
:root{{color-scheme:dark}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#080a0e;color:#e7eaf0;font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}}

/* ── header ── */
header{{padding:32px 32px 12px;border-bottom:1px solid #1a1d26;display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap}}
.header-left{{flex:1 1 auto}}
header h1{{font-size:24px;letter-spacing:.06em;font-weight:700;color:{ACCENT};margin-bottom:6px}}
header p{{color:#6b7285;font-size:12px;line-height:1.7;max-width:820px}}
.srv-badge{{font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;white-space:nowrap;cursor:default;transition:all .3s}}
.srv-badge.ok{{background:#0d2b1a;color:#3dca6e;border:1px solid #1a5c34}}
.srv-badge.off{{background:#2a0e0e;color:#e05555;border:1px solid #5c1a1a}}

/* ── file:// banner ── */
#file-banner{{display:none;background:#1a1000;border-bottom:2px solid {ACCENT};padding:12px 32px;font-size:13px;color:#c9a227;line-height:1.6}}
#file-banner strong{{color:#e7d08a}}
#file-banner a{{color:{ACCENT};font-weight:700;text-decoration:underline}}

/* ── grid ── */
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;padding:24px 32px 120px}}

/* ── card ── */
.card{{background:#0e1017;border-radius:12px;overflow:hidden;cursor:pointer;transition:transform .15s,box-shadow .15s,border-color .2s}}
.card:hover{{transform:translateY(-2px);box-shadow:0 6px 24px #0006}}
.card.selected{{border-color:{ACCENT} !important;box-shadow:0 0 0 2px {ACCENT}44 !important}}
.card-thumb img,.card-thumb video{{width:100%;display:block;aspect-ratio:16/9;object-fit:cover}}
.meta{{display:flex;align-items:center;gap:8px;padding:10px 12px 0;flex-wrap:wrap}}
.cut{{color:#080a0e;font-weight:900;font-size:11px;padding:3px 8px;border-radius:5px;letter-spacing:.02em}}
.tag{{font-size:11px;color:#7a8299;font-weight:600}}
.cap{{margin:7px 12px 3px;font-size:13px;color:#c8d0e0;line-height:1.5}}
.role{{margin:0 12px 12px;font-size:11px;color:{RED};font-weight:800}}
.updated-badge{{font-size:10px;background:#0d2b1a;color:#3dca6e;border:1px solid #1a5c34;padding:2px 7px;border-radius:10px;margin-left:auto}}
.updated-badge.vid{{background:#0d1f2b;color:#3da3ca;border-color:#1a455c}}

/* ── review panel ── */
#review-panel{{position:fixed;top:0;right:-440px;width:420px;height:100vh;background:#0d1018;border-left:1px solid #1e2330;padding:0;transition:right .25s cubic-bezier(.4,0,.2,1);overflow-y:auto;z-index:100;display:flex;flex-direction:column}}
#review-panel.open{{right:0}}
.panel-header{{padding:20px 20px 16px;border-bottom:1px solid #1e2330;display:flex;align-items:flex-start;gap:12px}}
.panel-header-info{{flex:1}}
#panel-cut-n{{font-size:20px;font-weight:900;color:{ACCENT};letter-spacing:.08em}}
#panel-cut-act{{font-size:11px;color:#7a8299;margin:2px 0}}
#panel-cut-scene{{font-size:12px;color:#9aa3b8;line-height:1.45;margin-top:4px}}
#panel-close{{background:none;border:none;color:#6b7285;font-size:20px;cursor:pointer;padding:4px 8px;border-radius:6px;line-height:1}}
#panel-close:hover{{color:#e7eaf0;background:#1e2330}}
.panel-body{{padding:20px;flex:1;display:flex;flex-direction:column;gap:18px}}
.prow{{display:flex;flex-direction:column;gap:8px}}
.plabel{{font-size:11px;font-weight:700;color:#7a8299;letter-spacing:.06em;text-transform:uppercase}}

/* mode toggle */
.mode-toggle{{display:flex;gap:6px}}
.mode-btn{{flex:1;padding:8px;border-radius:8px;border:1px solid #1e2330;background:#12151c;color:#8b93a7;font-size:13px;font-weight:600;cursor:pointer;transition:all .15s;text-align:center}}
.mode-btn.active{{border-color:{ACCENT};color:{ACCENT};background:#1a1500}}

/* select */
.panel-select{{width:100%;background:#12151c;border:1px solid #1e2330;color:#e7eaf0;font-size:13px;padding:9px 12px;border-radius:8px;outline:none;cursor:pointer}}
.panel-select:focus{{border-color:{ACCENT}}}

/* pills */
.pills{{display:flex;gap:6px;flex-wrap:wrap}}
.pill{{padding:6px 14px;border-radius:20px;border:1px solid #1e2330;background:#12151c;color:#8b93a7;font-size:12px;font-weight:600;cursor:pointer;transition:all .15s}}
.pill.active{{border-color:{ACCENT};color:{ACCENT};background:#1a1500}}

/* textarea */
#prompt-input{{width:100%;background:#12151c;border:1px solid #1e2330;color:#e7eaf0;font-size:13px;padding:12px;border-radius:8px;resize:vertical;min-height:90px;outline:none;font-family:inherit;line-height:1.5}}
#prompt-input:focus{{border-color:{ACCENT}}}
.input-hint{{font-size:11px;color:#454d63;margin-top:2px}}

/* gen button */
#gen-btn{{width:100%;padding:12px;border-radius:10px;border:none;background:{ACCENT};color:#080a0e;font-size:14px;font-weight:800;cursor:pointer;letter-spacing:.04em;transition:opacity .15s}}
#gen-btn:hover{{opacity:.88}}
#gen-btn:disabled{{opacity:.4;cursor:not-allowed}}

/* status */
.gen-status{{font-size:12px;font-weight:600;min-height:18px;text-align:center}}
.gen-status.loading{{color:#c9a227;animation:pulse 1.4s ease-in-out infinite}}
.gen-status.ok{{color:#3dca6e}}
.gen-status.err{{color:#e05555}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.5}}}}
</style>
</head><body>

<script id="cuts-data" type="application/json">{cuts_json_str}</script>

<header>
  <div class="header-left">
    <h1>{TITLE}</h1>
    <p>{SUB}</p>
  </div>
  <span id="srv-badge" class="srv-badge off" title="">○ 확인 중…</span>
</header>

<div id="file-banner">
  <strong>⚠ 파일로 직접 열었습니다.</strong>
  리뷰 서버를 먼저 실행한 뒤 아래 링크로 접속하세요:<br/>
  터미널: <code>python3 system_v2/_review_server.py</code> →
  <a id="srv-open-link" href="http://localhost:7800" target="_blank">http://localhost:7800</a> 에서 열기
</div>

<div class="grid">{''.join(cards_html)}</div>

<!-- ── Review Panel ── -->
<div id="review-panel">
  <div class="panel-header">
    <div class="panel-header-info">
      <div id="panel-cut-n">CUT —</div>
      <div id="panel-cut-act"></div>
      <div id="panel-cut-scene"></div>
    </div>
    <button id="panel-close" title="닫기 (Esc)">✕</button>
  </div>
  <div class="panel-body">

    <!-- 생성 타입 -->
    <div class="prow">
      <span class="plabel">생성 타입</span>
      <div class="mode-toggle">
        <button class="mode-btn active" id="mode-image">🖼 이미지</button>
        <button class="mode-btn" id="mode-video">▶ 영상</button>
      </div>
    </div>

    <!-- 이미지 모델 -->
    <div class="prow" id="img-model-wrap">
      <span class="plabel">이미지 모델</span>
      <select class="panel-select" id="img-model-sel">{img_opts}</select>
    </div>

    <!-- 이미지 해상도 -->
    <div class="prow" id="img-res-row" style="display:flex">
      <span class="plabel">해상도</span>
      <div class="pills">
        <button class="pill pill-iq" data-val="1k">1k</button>
        <button class="pill pill-iq active" data-val="2k">2k</button>
        <button class="pill pill-iq" data-val="4k">4k</button>
      </div>
    </div>

    <!-- 영상 모델 -->
    <div class="prow" id="vid-model-wrap" style="display:none">
      <span class="plabel">영상 모델</span>
      <select class="panel-select" id="vid-model-sel">{vid_opts}</select>
    </div>

    <!-- 영상 전용 옵션 -->
    <div id="video-opts" style="display:none;display:flex;flex-direction:column;gap:14px">
      <div class="prow">
        <span class="plabel">길이</span>
        <div class="pills">
          <button class="pill pill-dur" data-val="3">3초</button>
          <button class="pill pill-dur" data-val="4">4초</button>
          <button class="pill pill-dur active" data-val="5">5초</button>
          <button class="pill pill-dur" data-val="8">8초</button>
        </div>
      </div>
      <div class="prow">
        <span class="plabel">화질</span>
        <div class="pills">
          <button class="pill pill-vq" data-val="720p">720p</button>
          <button class="pill pill-vq active" data-val="1080p">1080p</button>
        </div>
      </div>
    </div>

    <!-- 수정 요청 -->
    <div class="prow" style="flex:1">
      <span class="plabel">수정 요청사항</span>
      <textarea id="prompt-input" placeholder="수정 요청사항을 입력하세요…"></textarea>
      <span class="input-hint">Enter = 생성 · Shift+Enter = 줄바꿈</span>
    </div>

    <!-- 생성 버튼 & 상태 -->
    <div class="prow" style="gap:10px">
      <button id="gen-btn">↵ 생성 시작</button>
      <div class="gen-status" id="gen-status"></div>
    </div>

  </div>
</div>

<script>{JS}</script>
</body></html>"""

    outpath = os.path.join(PREVIEW_DIR, OUTFILE)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = round(os.path.getsize(outpath) / 1024 / 1024, 2)
    print(f"saved: {outpath}  ({size_mb} MB)")
    print(f"review server: python3 system_v2/_review_server.py")


if __name__ == "__main__":
    main()
