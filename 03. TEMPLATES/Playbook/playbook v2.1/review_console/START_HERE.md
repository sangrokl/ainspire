# ▶ 여기서 시작 (AETHER 리뷰 콘솔 번들)

이 폴더는 **롤플레잉 튜토리얼**(`../tutorial_shoot_script_AETHER.md`)과 함께 쓰는 **리뷰·수정 콘솔**입니다.
바로 옆 `../v2026-05-29_v4` 의 AETHER 최종 스토리보드 이미지를 띄워, 카드를 골라 수정 요청을 보낼 수 있습니다.

## 1) 처음 한 번 (파이썬 패키지 설치)
```
pip install -r requirements.txt
```
(파이썬 3.9+ 필요. Pillow 한 개만 씁니다.)

## 2) 실행
- **Windows**: `run_aether_image.bat` **더블클릭**
- **mac/linux**: `bash run_aether_image.sh`
- 또는 직접:
  ```
  python start.py --media-dir "../v2026-05-29_v4" --mode image --backend agent --title "AETHER 스토리보드 리뷰"
  ```
→ 브라우저가 `http://localhost:8765/` 로 자동 오픈됩니다.

## 3) 사용
- 카드를 **클릭해 선택** → 모델(`nano_banana_2`/`gpt_image_2`)·화질 고르고 → **수정 요청 입력 → Enter**
- 영상 리뷰가 필요하면 `--mode video --media-dir "<영상 폴더>"` 로 실행

## 모든 생성 = Higgsfield MCP 전용
- `--backend mock`(기본): API 없이 **UI·흐름 데모**(원본에 '수정본' 라벨).
- `--backend agent`(실가동): 워커는 큐만 쌓고, **Claude 에이전트가 Higgsfield MCP로 실제 재생성**합니다.
  → Claude 세션에서 **"리뷰 큐 처리해줘"** 라고 하면 `runtime/revision_queue.jsonl` 을 읽어
  `generate_image`(nano_banana_2/gpt_image_2) · `generate_video`(seedance_2_0) 로 처리하고
  결과를 `runtime/results.json` 에 반영 → 콘솔이 자동 갱신합니다. (자세히: `AGENT_QUEUE_GUIDE.md`)

## 다른 컴퓨터로 옮기기
이 폴더가 들어있는 **`aether_energy/` 폴더를 통째로 복사**하면 됩니다.
(런처가 상대경로 `../v2026-05-29_v4` 를 쓰므로 경로 그대로 동작)

> 더 자세한 설명: `README.md`
