# -*- coding: utf-8 -*-
"""
리뷰 콘솔 HTML 빌더 (이미지/영상 모드).
완성 스토리보드(storyboard_AETHER_FINAL...) 디자인을 계승한 다크 카드 그리드 +
카드별 [선택 → 수정요청 입력 → Enter] 인라인 수정 UI + 결과 폴링 JS 를 생성한다.

미디어는 base64로 박지 않고 로컬 서버의 /media/<파일> 경로로 참조한다(가벼움).
사용: python build_console.py --media-dir <폴더> --mode image|video --title "..." --out webroot/console.html
"""
import argparse, os, re, html
from pathlib import Path

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
VID_EXT = {".mp4", ".webm", ".mov"}

def natkey(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]

def disp_num(stem, idx):
    m = re.findall(r"\d+", stem)
    return f"{int(m[-1]):02d}" if m else f"{idx+1:02d}"

def list_media(media_dir, mode):
    exts = IMG_EXT if mode == "image" else VID_EXT
    files = []
    for p in sorted(Path(media_dir).iterdir(), key=lambda x: natkey(x.name)):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        if p.name.startswith(".") or p.name.startswith("_") or " " in p.name or "[" in p.name:
            continue  # 숨김/수정본/스트레이 파일 제외
        files.append(p.name)
    return files

CSS = """
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:#0b0d12;color:#e7eaf0;font-family:'Pretendard','Apple SD Gothic Neo',system-ui,sans-serif}
header{padding:34px 28px 6px;position:sticky;top:0;background:linear-gradient(#0b0d12,#0b0d12ee);z-index:5}
header .kick{font-size:12px;letter-spacing:.18em;color:#6f7891;text-transform:uppercase;margin-bottom:6px}
header h1{margin:0 0 6px;font-size:24px;letter-spacing:-.02em;color:__ACCENT__}
header .tag{margin:0;color:#aeb6c8;font-size:13px;line-height:1.55}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:12px 28px;border-bottom:1px solid #1e2330}
.bar .sp{flex:1}
.bar button{background:__ACCENT__;color:#08110d;border:0;font-weight:800;font-size:13px;padding:9px 14px;border-radius:9px;cursor:pointer}
.bar button.ghost{background:transparent;color:__ACCENT__;border:1px solid __ACCENT__}
.bar .hint{font-size:12px;color:#6f7891}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:18px 28px 60px}
.card{background:#12151c;border:1px solid #1e2330;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:border-color .15s,box-shadow .15s}
.card.sel{border-color:__ACCENT__;box-shadow:0 0 0 2px __ACCENT__55}
.thumbwrap{position:relative;cursor:pointer}
.thumbwrap img,.thumbwrap video{width:100%;display:block;aspect-ratio:16/9;object-fit:cover;background:#000}
.tick{position:absolute;top:8px;left:8px;width:22px;height:22px;border-radius:6px;border:2px solid #ffffffaa;background:#0008;display:flex;align-items:center;justify-content:center;font-size:13px;color:transparent}
.card.sel .tick{background:__ACCENT__;border-color:__ACCENT__;color:#08110d}
.meta{display:flex;align-items:center;gap:8px;padding:9px 12px 0;flex-wrap:wrap}
.cut{color:#08110d;font-weight:800;font-size:12px;padding:2px 9px;border-radius:6px;background:__ACCENT__}
.chip{font-size:11px;font-weight:700;padding:2px 8px;border-radius:20px;background:#1b2230;color:#9aa3b5}
.chip.wait{background:#1b2230;color:#9aa3b5}
.chip.run{background:#3a2d10;color:#ffcf6b}
.chip.done{background:#10301f;color:#5be0a0}
.chip.err{background:#3a1414;color:#ff8a8a}
.panel{max-height:0;overflow:hidden;transition:max-height .2s;padding:0 12px}
.card.sel .panel{max-height:260px;padding:10px 12px 14px}
.row{display:flex;gap:8px;margin-bottom:8px}
.row select{flex:1;background:#0e1117;color:#dfe5f0;border:1px solid #283042;border-radius:8px;padding:7px 8px;font-size:12px}
.req{width:100%;min-height:54px;background:#0e1117;color:#fff;border:1px solid #283042;border-radius:8px;padding:8px 10px;font-size:13px;resize:vertical;font-family:inherit}
.req:focus{outline:0;border-color:__ACCENT__}
.hk{font-size:11px;color:#6f7891;margin-top:5px}
"""

PAGE = """<!doctype html><html lang="ko"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/><title>__TITLE__</title>
<style>__CSS__</style></head><body>
<header>
  <div class="kick">REVIEW CONSOLE · __MODEUP__</div>
  <h1>__TITLE__</h1>
  <p class="tag">카드를 클릭해 선택 → 수정 요청을 입력하고 <b>Enter</b> → 즉시 재생성. (Shift+Enter 줄바꿈)</p>
</header>
<div class="bar">
  __BATCHBTN__
  <span class="hint">기본값은 카드마다 바꿀 수 있어요</span>
  <span class="sp"></span>
  <span class="hint" id="poll">연결됨 · 자동 갱신</span>
</div>
<div class="grid">__CARDS__</div>
<script>
const MODE="__MODE__";
function chip(card,cls,txt){const c=card.querySelector('[data-chip]');c.className='chip '+cls;c.textContent=txt;}
document.querySelectorAll('.thumbwrap').forEach(t=>{
  t.addEventListener('click',()=>{t.closest('.card').classList.toggle('sel');});
});
document.querySelectorAll('.req').forEach(inp=>{
  inp.addEventListener('keydown',e=>{
    if(e.key==='Enter' && !e.shiftKey){
      e.preventDefault();
      const card=inp.closest('.card');
      if(!inp.value.trim())return;
      const payload={type:MODE,cut:card.dataset.cut,request:inp.value.trim()};
      if(MODE==='image'){payload.model=card.querySelector('.model').value;payload.quality=card.querySelector('.quality').value;}
      else{payload.duration=parseInt(card.querySelector('.duration').value);payload.quality=card.querySelector('.quality').value;}
      chip(card,'run','처리중…');
      fetch('/revise',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
        .then(r=>r.ok?null:Promise.reject()).catch(()=>chip(card,'err','전송 실패'));
    }
  });
});
const batch=document.getElementById('batchVideo');
if(batch){batch.addEventListener('click',()=>{
  if(!confirm('확정 스토리보드 전체를 영상으로 생성할까요?'))return;
  fetch('/revise',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({type:'batch_video',duration:4,quality:'1080p'})}).then(()=>batch.textContent='영상 생성 요청됨 ✓');
});}
// 결과 폴링: 완료된 카드 썸네일/상태 자동 교체
async function poll(){
  try{
    const r=await fetch('/results?t='+Date.now()); const data=await r.json();
    for(const cut in data){
      const card=document.querySelector('.card[data-cut="'+CSS.escape(cut)+'"]'); if(!card)continue;
      const st=data[cut];
      if(st.status==='done'){chip(card,'done','완료');
        if(st.src){const m=card.querySelector('img,video');if(m)m.src=st.src+'?t='+(st.ts||Date.now());}}
      else if(st.status==='error'){chip(card,'err',st.msg||'실패');}
      else if(st.status==='running'){chip(card,'run','처리중…');}
    }
  }catch(e){document.getElementById('poll').textContent='서버 연결 끊김';}
}
setInterval(poll,4000); poll();
</script>
</body></html>"""

def build(media_dir, mode, title, out, accent):
    files = list_media(media_dir, mode)
    cards = []
    for i, fn in enumerate(files):
        stem = os.path.splitext(fn)[0]
        num = disp_num(stem, i)
        src = "/media/" + fn
        if mode == "image":
            media_el = f'<img src="{src}" alt="{num}"/>'
            controls = (
                '<div class="row">'
                '<select class="model"><option value="nano_banana_2">nano_banana_2 (Higgsfield)</option>'
                '<option value="gpt_image_2">gpt_image_2 (Higgsfield)</option></select>'
                '<select class="quality"><option>1k</option><option selected>2k</option><option>4k</option></select>'
                '</div>')
        else:
            media_el = f'<video src="{src}" autoplay muted loop playsinline preload="metadata"></video>'
            controls = (
                '<div class="row">'
                '<select class="duration"><option selected>4</option><option>6</option><option>8</option></select>'
                '<select class="quality"><option>480p</option><option>720p</option><option selected>1080p</option></select>'
                '</div>')
        cards.append(f"""
  <div class="card" data-cut="{html.escape(stem)}">
    <div class="thumbwrap"><span class="tick">✓</span>{media_el}</div>
    <div class="meta"><span class="cut">C{num}</span><span class="chip wait" data-chip>대기</span></div>
    <div class="panel">
      {controls}
      <textarea class="req" placeholder="이 컷의 수정 요청을 한글로 입력하고 Enter"></textarea>
      <div class="hk">Enter=재생성 요청 · Shift+Enter=줄바꿈</div>
    </div>
  </div>""")
    batchbtn = '<button id="batchVideo">▶ 전체 영상으로 돌리기</button>' if mode == "image" else \
               '<span class="hint">영상 리뷰 · 컷별 초수/화질 선택 후 Enter</span>'
    page = (PAGE
            .replace("__TITLE__", html.escape(title))
            .replace("__CSS__", CSS.replace("__ACCENT__", accent))
            .replace("__MODE__", mode).replace("__MODEUP__", mode.upper())
            .replace("__BATCHBTN__", batchbtn)
            .replace("__CARDS__", "".join(cards)))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(page, encoding="utf-8")
    print(f"[build_console] {mode} · {len(files)} cards -> {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--media-dir", required=True)
    ap.add_argument("--mode", choices=["image", "video"], default="image")
    ap.add_argument("--title", default="리뷰 콘솔")
    ap.add_argument("--out", default="webroot/console.html")
    ap.add_argument("--accent", default="#3aa0ff")
    a = ap.parse_args()
    build(a.media_dir, a.mode, a.title, a.out, a.accent)
