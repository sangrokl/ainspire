# VELVET NOIR — 리뷰 서버 워크플로우

## 서버 개요

`system_v2/_review_server.py` 가 포트 7800에서 실행되어야 HTML 스토리보드의 기능이 활성화된다.

- HTML 파일: `v20260626/preview/storyboard_VELVET_NOIR_30cut_v20260626.html`
- HTML을 `file://`로 열면 JS가 자동으로 `http://localhost:7800` 을 서버 주소로 사용
- 서버가 없으면 영상 로드·컷 수정·재생성 기능이 전부 실패

---

## 서버 시작 (백그라운드)

플레이북 루트(`playbook v2.1/`)에서 실행:

```bash
cd "/Volumes/LEARN (4TB)/ Claude/02. Learn/03. TEMPLATES/Playbook/playbook v2.1"

nohup python3 system_v2/_review_server.py \
  --project VELVET_NOIR \
  --version v20260626 \
  --port 7800 \
  > /tmp/review_server_velvet_noir.log 2>&1 &

echo "PID: $!"
```

시작 확인:

```bash
curl -s http://localhost:7800/api/status
# → {"ok": true, "project": "VELVET_NOIR", "version": "v20260626"}
```

---

## 서버 종료

```bash
# PID로 종료
kill <PID>

# 또는 포트로 찾아서 종료
kill $(lsof -ti :7800)
```

---

## 자동 주입 내용

서버는 `/api/regenerate` 요청마다 다음을 자동 주입한다:

1. **규칙0[A]** — 앵글·백라이트·네거티브필 강제 규칙
2. **IMG_ENHANCE** — ARRI 그레인·시네마틱 품질 상수
3. **NOIR_DESC** — 주인공 캐릭터 설명 (로고·병 컷 제외)
4. **씬 컨텍스트** — `scenario.md`의 `[first frame]` / `[video prompt]`
5. **ref 이미지** — 컷 종류에 따라 얼굴 ref / 병 ref / 로고 ref 자동 선택

| 컷 종류 | 주입 ref |
|---------|---------|
| 일반 캐릭터 컷 | `assets/ref/main_character/ref_face_v3.png` |
| 병 컷 (8·25·26·27·28) | `assets/ref/product/ref_bottle_v2.png` |
| 로고 컷 (29·30) | `assets/ref/logo/logo_A_serif_wordmark.png` |
| 컷 30 (병+로고) | 병 ref + 로고 ref 둘 다 |

---

## API 엔드포인트

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /api/status` | 서버 상태 확인 |
| `GET /api/images/<파일명>` | 이미지 컷 서빙 |
| `GET /api/videos/<파일명>` | 영상 컷 서빙 |
| `GET /api/scene?n=<컷번호>` | 시나리오 씬 데이터 반환 |
| `POST /api/regenerate` | 컷 재생성 (Higgsfield CLI) |

---

## 재생성 저장 경로

- 이미지: `v20260626/assets/images/cut_NN_v1.png`, `_v2.png`, …
- 영상: `v20260626/assets/videos/cut_NN_v1.mp4`, `_v2.mp4`, …
- 원본(`cut_NN.png` / `cut_NN.mp4`)은 덮어쓰지 않음

---

## 스토리보드 HTML 갱신 (수정본 반영)

수정본(`cut_NN_vX.png` / `cut_NN_vX.mp4`)이 생긴 뒤 HTML에 반영하려면 빌드 스크립트를 재실행한다.

```bash
cd "/Volumes/LEARN (4TB)/ Claude/02. Learn/03. TEMPLATES/Playbook/playbook v2.1"
python3 system_v2/_build_VELVET_NOIR_embed.py
```

**동작 방식:**
- 빌드 스크립트는 각 컷마다 `cut_NN_vX` 중 가장 높은 버전을 자동 선택
- 이미지: 최신 버전을 base64로 HTML에 임베드
- 영상: `data-src="/api/videos/cut_NN_vX.mp4"` 로 최신 버전 참조
- 버전이 없으면 원본(`cut_NN.png` / `cut_NN.mp4`)으로 폴백

**버전 선택 우선순위:** `cut_NN_v3` > `cut_NN_v2` > `cut_NN_v1` > `cut_NN` (원본)
