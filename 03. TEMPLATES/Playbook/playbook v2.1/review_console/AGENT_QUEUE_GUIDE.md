# 🤖 AGENT_QUEUE_GUIDE — Claude 에이전트가 수정 큐를 처리하는 법

이 콘솔은 **콘솔 UI·로컬 서버·큐**를 담당하고, **모든 이미지·영상 생성은 Higgsfield MCP 전용**이다.
이미지(`nano_banana_2`/`gpt_image_2`)·영상(`seedance_2_0`) 전부 MCP라 `worker.py`가 직접 못 부른다 →
**Claude 에이전트(이 세션)가 큐를 읽어 Higgsfield MCP로 처리**한다. (CometAPI 등 직접호출 경로 미사용)

## 트리거
사용자가 콘솔에서 Enter로 보낸 요청은 `runtime/revision_queue.jsonl` 에 한 줄씩 쌓인다.
사용자가 **"리뷰 큐 처리해줘"** 라고 하면(또는 백그라운드 워처 에이전트를 띄워두면) 아래를 수행.

## 처리 루프 (에이전트)
1. `review_console/runtime/revision_queue.jsonl` 의 **새 줄**을 읽는다(이미 처리한 줄 수는 `runtime/.agent_offset`로 추적).
2. 각 항목 `{type, cut, request, model, quality, duration}` 마다:
   - **이미지 (model `nano_banana_2` 또는 `gpt_image_2`) — 둘 다 Higgsfield**:
     - 원본: `MEDIA_DIR/<cut>.<ext>` 를 `media_upload` → `media_confirm`
     - `generate_image({ model:<item.model>, prompt:request, medias:[{role:"image", value:<media_id>}], resolution:quality(1k/2k/4k) })`
     - 결과 PNG를 `MEDIA_DIR/_revisions/<cut>_rev<k>.png` 로 다운로드
   - **영상(type `video`, model `kling3_0_turbo` 또는 `seedance_2_0`)**:
     - 원본 컷 이미지를 `media_upload`/`media_confirm`
     - **`kling3_0_turbo`** (UI 기본값): `generate_video({ model:"kling3_0_turbo", prompt:request, duration, resolution:quality(720p/1080p), aspect_ratio:"16:9", medias:[{role:"start_image", value:<media_id>}] })` — duration 범위 3–15s.
     - **`seedance_2_0`**: `generate_video({ model:"seedance_2_0", prompt:request, duration, resolution:quality(480p/720p/1080p), generate_audio:false, medias:[{role:"start_image", value:<media_id>}] })` — `generate_audio:false` 필수(No-BGM 규칙). duration 범위 4–15s.
     - 완료 폴링 후 mp4를 `MEDIA_DIR/_revisions/<cut>_rev<k>.mp4` 로 다운로드
   - **`batch_video`**: 콘솔의 [전체 영상으로 돌리기]. 폴더의 모든 컷 이미지를 위 영상 절차로 일괄 생성(동시 8 한도 큐). item의 model 필드 우선 사용(없으면 `kling3_0_turbo` 기본).
3. 각 항목 완료 시 `runtime/results.json[cut] = { "status":"done", "src":"/media/_revisions/<파일>", "ts":<유닉스초> }` 로 갱신 → 콘솔이 자동으로 썸네일 교체.
4. 실패는 GATE 12 핸들링(502 재시도 · `declined_preset_id` · NSFW 표현 우회 · `fetch failed` 재시도) 그대로. 실패 시 `{"status":"error","msg":"..."}`.

## 규칙
- **동시 8개 한도** 준수(Higgsfield). 9개+면 큐로.
- **재생성은 새 파일**(`_revisions/`)로 — 원본 보존(절대 규칙).
- 폴링·다운로드가 길면 **백그라운드 에이전트**에 위임(메인 컨텍스트 보호).
- `results.json` 의 `src` 는 반드시 `/media/...` 형태(로컬 서버가 서빙) — 콘솔이 그 경로로 즉시 로드.

## results.json 예시
```json
{
  "halo_c09": { "status": "done", "src": "/media/_revisions/halo_c09_rev1.png", "ts": 1764500000 },
  "halo_c21": { "status": "running", "msg": "seedance 생성 중" }
}
```

> 요약: **사람은 콘솔에서 클릭·타이핑만**, 큐 적재는 로컬 서버, **MCP 생성은 에이전트**, 결과는 콘솔이 자동 반영.
