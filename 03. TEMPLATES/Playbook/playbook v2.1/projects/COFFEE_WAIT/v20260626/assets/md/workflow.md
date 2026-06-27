# COFFEE_WAIT — 리뷰 서버 워크플로우

## 프로젝트 개요

- **브랜드**: Lento (프리미엄 커피 파우치)
- **로그라인**: 이름도 얼굴도 모르는 누군가를 기다리며 보내는 며칠. 커피 한 잔이 그 기다림을 조용히 함께한다.
- **버전**: v20260626
- **포트**: 7801 (VELVET_NOIR 7800과 구분)

## 서버 개요

`system_v2/_review_server.py` 가 포트 7801에서 실행되어야 HTML 스토리보드의 기능이 활성화된다.

- HTML 파일: `v20260626/preview/storyboard_COFFEE_WAIT_video_v20260626.html`
- 서버가 없으면 영상 로드·컷 수정·재생성 기능이 전부 실패

---

## 서버 시작 (백그라운드)

플레이북 루트(`playbook v2.1/`)에서 실행:

```bash
cd "/Volumes/LEARN (4TB)/ Claude/02. Learn/03. TEMPLATES/Playbook/playbook v2.1"

nohup python3 system_v2/_review_server.py \
  --project COFFEE_WAIT \
  --version v20260626 \
  --port 7801 \
  > /tmp/review_server_coffee_wait.log 2>&1 &

echo "PID: $!"
```

시작 확인:

```bash
curl -s http://localhost:7801/api/status
# → {"ok": true, "project": "COFFEE_WAIT", "version": "v20260626"}
```

---

## 서버 종료

```bash
kill $(lsof -ti :7801)
```

---

## ref 이미지

| 종류 | 경로 |
|------|------|
| 캐릭터 얼굴 | `assets/ref/main_character/ref_face.png` |
| 로고 (다크) | `assets/ref/logo/lento_dark.png` |
| 로고 (라이트) | `assets/ref/logo/lento_light.svg` |

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
- 원본은 덮어쓰지 않음

---

## 현재 실행 중인 서버 목록

| 프로젝트 | 포트 |
|---------|------|
| VELVET_NOIR | 7800 |
| COFFEE_WAIT | 7801 |

---

## 📁 버전 폴더 표준 구조 (모든 프로젝트 공통)

> 새 프로젝트를 시작할 때, 그리고 파일을 저장할 때마다 아래 구조를 반드시 따른다.

```
projects/{PROJECT}/
└── {VERSION}/                  ← 버전 폴더 (예: v20260626)
    ├── assets/                 ← 모든 생성 소재 — 탑레벨 노출
    │   ├── audio/              ← TTS · VO · SFX · BGM
    │   │   ├── bgm/
    │   │   └── vo/
    │   ├── images/             ← 생성 이미지 컷 (cut_NN.png, cut_NN_vX.png)
    │   ├── videos/             ← 생성 영상 컷 (cut_NN.mp4, cut_NN_vX.mp4)
    │   ├── md/                 ← 문서 (scenario.md, workflow.md, manifest.json 등)
    │   └── ref/                ← 참조 원본 — 수정 금지
    │       ├── logo/
    │       ├── product/
    │       └── main_character/
    ├── output/                 ← 최종 조립 영상 · 내보내기
    └── preview/                ← 스토리보드 HTML · 영상 리뷰 HTML
```

**규칙:**
- 탑레벨(`{VERSION}/` 바로 아래)에는 `assets/` · `output/` · `preview/` **3개 폴더만** 노출
- 낱개 파일(.html, .md, .json 등)을 탑레벨에 두지 않는다
- `workflow.md`는 반드시 `{VERSION}/assets/md/workflow.md`에 저장
- 이미지·영상 수정본은 `cut_NN_v1.png`, `_v2.png` 형식으로 신규 저장 (원본 덮어쓰기 금지)
