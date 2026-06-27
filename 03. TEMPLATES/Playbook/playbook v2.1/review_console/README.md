# 🎛️ Review Console — 스토리보드/영상 인라인 수정 콘솔 (포터블 패키지)

스토리보드 이미지·영상을 **카드 그리드 HTML로 띄우고**, 카드를 **선택 → 수정요청 입력 → Enter** 하면
그 컷만 **즉시 재생성**되는 도구. 디자인은 완성 스토리보드(`storyboard_AETHER_FINAL...html`) 스타일을 계승.

> **다른 컴퓨터에서도** 이 `review_console/` 폴더만 통째로 복사하면 됩니다. (파이썬 표준 라이브러리 + Pillow)

---

## 빠른 시작 (3줄)

```bash
cd review_console
pip install -r requirements.txt
python start.py --media-dir "../projects/AETHER_ENERGY/v2026-05-29_v4" --mode image --backend agent --title "AETHER 리뷰"
```
→ 브라우저가 `http://localhost:8765/` 로 자동 오픈. 카드 클릭 → 수정요청 입력 → **Enter**.

영상 리뷰:
```bash
python start.py --media-dir "../projects/HALO_WATCH/v2026-05-29_v9/assets/videos" --mode video --backend agent --title "HALO 영상 리뷰"
```

---

## 동작 구조 (브리지)

```
[브라우저 콘솔]  카드 선택→입력→Enter
     │ POST /revise {type,cut,request,model/duration,quality}
     ▼
[review_server.py]  →  runtime/revision_queue.jsonl 에 append
     ▼
[worker.py]  큐를 읽어 재생성 → MEDIA_DIR/_revisions/ 에 저장 → runtime/results.json 갱신
     ▼
[콘솔]  /results 4초 폴링 → 카드 썸네일/상태 자동 교체
```

---

## 백엔드 (`--backend`) — ★ 모든 생성은 Higgsfield MCP 전용

| 값 | 동작 | 필요 |
|---|---|---|
| `mock` (기본) | 원본에 '수정본' 라벨을 얹어 즉시 교체 — **오프라인 UI 데모**로 전체 흐름 확인 | 없음 |
| `agent` | **실가동.** 워커는 항목을 `needs-agent`로 표시만 하고, **Claude 에이전트가 Higgsfield MCP**로 재생성 | Higgsfield MCP(연결된 Claude 세션) |

> **이미지(`nano_banana_2` / `gpt_image_2`)·영상(`seedance_2_0`) 전부 Higgsfield MCP** 로만 생성한다.
> MCP 는 Claude 에이전트만 호출할 수 있으므로, worker 는 직접 생성하지 않고 큐만 관리한다.
> 실제 재생성은 **Claude 에이전트가 [AGENT_QUEUE_GUIDE.md](./AGENT_QUEUE_GUIDE.md)** 대로 큐를 읽어 처리하고 `results.json` 을 갱신 → 콘솔이 자동 반영.
> (별도 API 키 불필요 — Higgsfield 는 MCP OAuth. CometAPI 등 직접호출 경로는 사용하지 않음.)

---

## 설정

`config.example.json` → `config.json` 으로 복사하거나 환경변수로 준다. (생성에 별도 키 불필요)

```json
{ "port": 8765, "backend": "mock" }
```

---

## UI 요약

- **이미지 카드**: 모델(`nano_banana_2`/`gpt_image_2`) · 화질(1k/2k/4k) · 수정요청 + Enter
- **영상 카드**: 모델(`kling3_0_turbo`/`seedance_2_0`) · 초수(4/5/6/8s) · 화질(480/720/1080p) · 수정요청 + Enter
- 상단 **[전체 영상으로 돌리기]**(이미지 모드): 확정 스토리보드를 한 번에 영상화 요청(에이전트 처리)
- 상태칩: 대기 → 처리중 → 완료(썸네일 교체)

## 파일

| 파일 | 역할 |
|---|---|
| `start.py` | 원클릭(빌드+서버+워처+브라우저) |
| `build_console.py` | 콘솔 HTML 생성(이미지/영상) |
| `review_server.py` | 로컬 서버(`/`,`/media`,`/results`,`/revise`) |
| `worker.py` | 큐 워처(mock/agent) — 생성은 Higgsfield MCP 전용 |
| `AGENT_QUEUE_GUIDE.md` | Claude 에이전트가 nano_banana_2/seedance 처리하는 법 |
| `webroot/`,`runtime/` | 생성물(콘솔 HTML, 큐/결과) — 자동 생성 |

## 안전

- 서버는 `127.0.0.1`(로컬)만 바인딩. `/media` 는 경로 탈출 차단.
- 모든 재생성은 `MEDIA_DIR/_revisions/` 에 **새 파일**로 저장(원본 보존).
