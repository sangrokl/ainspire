# 04_reference_lessons-appendix.md — 시행착오·부록 (필요 시 로드)

> ENHANCE 상수 풀텍스트는 `03_reference_enhance-prompts.md` 참조. 이 파일에서는 세션 맥락 설명만 유지하고 상수 본문을 중복 수록하지 않는다.

---

## 부록 A — 시행착오 한눈에 (Lessons Learned)
이번 AETHER·HALO(컨셉 v1→v10 + 영상·내레이션·로고 전 과정)에서 실제로 배운 것:

1. **상표는 디자인 언어로** — 브랜드명 직접 입력 금지(필터·법적).
2. **제품 매 컷 노출 = 촌스러움** — 감정 서사에 녹이고 히어로샷은 피날레로. (B형 추천)
3. **기능 나열 ≠ 스토리** — 한 주인공의 감정 아크.
4. **공간/인물 과다 = 산만** — 1~2 공간으로 압축, 교차·반복으로 공감 밀도.
5. **2번째 인물은 실루엣/손/뒷모습/화면** — 얼굴 일관성 문제 회피.
6. **빈 배경 = 싸 보임** — `ARTDIR`로 화면 꽉 채우기 + 컬러콘트라스트 전 컷 공통 적용.
7. **얼굴/제품은 img2img ref로 락**, 의상만 교체 지시.
8. **`fetch failed` / 일시 오류** — 실패 컷만 재시도하면 풀림. (Higgsfield 기준)
9. **거대 종료코드 = 프로세스 사망** — 디스크 확인 후 빠진 것만 재생성.
10. **이미지를 Read로 열지 말 것**, **생성 전 4종+프리뷰 승인**, **수정=새 버전**.
11. **큰 컨셉 분기는 비싼 생성 전에 객관식으로 먼저 확정** — 30컷을 헛돌리지 않는 가장 큰 절약.
12. **의상 교체가 얼굴을 흔든다** — 시그니처 룩 1개로 통일하고, "동일 얼굴·머리·나이 절대 변경 금지(IDENTITY 상수)"를 강하게 박는다.
13. **2번째 인물은 강한 네거티브로 못박아라** — "얼굴 절대 노출 금지, 새 인물·낯선 얼굴 금지, 순수 그림자/뒷모습/손만(NEG_OTHER)"을 명시.
14. **제품 단독 매크로 컷에 사람·손이 샌다** — "PRODUCT ONLY, NO people, NO hands, NO wrist, NO body parts, just the watch"로 못박는다.
15. **막히면 레퍼런스를 분석하라** — 무한 재생성 말고, 실존 명작 광고를 웹 검색·분석해 문법을 빌려 다시 제안.
16. **영상은 동시 8개 한도** — 8개씩 큐, 폴링·다운로드는 백그라운드 에이전트 위임. `declined_preset_id`로 프리셋 강제 거절, NSFW 오탐(포옹)은 표현 우회.
17. **BGM은 API 자동생성 안 함 → Suno 프롬프트 제안 + 사용자 수동 생성(GATE 13)** — 생성 영상 자체는 SFX only, BGM은 후반 조립에서 얹는다.
18. **내레이션은 비트 매핑 + 톤별 성우** — 막 시작 컷에 한 줄씩 타임코드 매핑. 차분=stability↑/style↓, 강렬=반대. **기본은 ElevenLabs MCP(`text_to_speech`)** — 이 환경에 연결되어 있으면 별도 키·`.env` 불필요. 백업1 Higgsfield TTS(`inworld_text_to_speech`, Higgsfield 연결만 있으면 됨) · 백업2 ElevenLabs 직접 API 쓸 때만 `ELEVENLABS_API_KEY`(`.env`) 필요(내레이션 자체는 선택 산출물).
19. **로고는 블랙 생성 → 루마키 투명 → 오토크롭**. 짧은 단어도 철자 검수. 제품 워드마크 가로화는 목업 img2img.
20. **최종 완성본은 기획안+VO+컷을 한 HTML로** — 이미지는 최종 버전 폴더 소스, `_FINAL` 새 파일(덮어쓰기 금지).
21. **리뷰는 채팅이 아니라 콘솔로(GATE 17)** — 생성 후 리뷰 HTML 자동 팝업 → 카드 선택→수정요청 Enter→즉시 재생성. HTML은 MCP를 직접 못 부르니 **로컬서버+큐+에이전트 워처** 브리지로 잇고, 이미지=nano_banana_2/gpt_image_2(모델·화질 선택), 영상=Seedance 2.0 Mini(초수·화질 선택, 백업1 Fast→백업2 standard). 재생성은 새 버전 폴더.

---

## 부록 B — 이 플레이북으로 만들어진 실제 사례 (전 과정)

- **HALO**(스마트워치) **최종 = 애플워치 〈911〉 문법 「몇 분을 가른 신호」**: 고독한 산악 트레일 사고 → 워치 낙상감지·SOS·비콘 → 구조 → 안도. 제품 히어로는 피날레 6컷.
  - 컨셉 여정: 거리(연결) → 회복/자기돌봄/도전 제안 전부 거부 → **레퍼런스 분석으로 911 채택**. 일관성 강화(시그니처 룩·페이스리스)로 v6, 영상화용 시네마틱·로우키 재촬영 v8, 인물오류 수정 v9, 배경 수정 v10.
  - 제작: Seedance 4초×30컷(컷별 카메라무브, 8-동시 큐) + 다큐 내레이션 3안(차분 미국 남성) + 로고 + 최종 완성 스토리보드(v10 이미지).
- **AETHER**(에너지드링크): 무채색 번아웃 → 음료로 일렉트릭 블루 코스믹 에너지 충전 → 색이 돌아온 자신감 복귀(3막 변신). 프리미엄 보정 v2/v3 + 터프 중저음 내레이션 3안 + 로고/가로 워드마크 + 최종 완성 스토리보드(v3 프리미엄 이미지).

---

## 부록 C — 검증된 풀 파이프라인 자동화 (재사용 표준)

기획→스토리보드→영상→오디오(VO)→**프리미어 자동 편집**까지 한 번에 돌린 실전 흐름. 모든 생성에 `IMG_ENHANCE`/`VID_ENHANCE`(→ `03` 참조)를 기본 주입한다.

### C-1. 이미지 30컷 — Higgsfield + Magnific 2엔진 병렬 생성 (시간 절반)
- **Higgsfield + Magnific 병렬**(서로 다른 풀이라 한도가 합쳐진다 — Higgsfield 계정당 8동시 + Magnific 이미지 단위 24동시). 막 단위로 분담하거나, 같은 컷을 양쪽에서 동시 생성 후 베스트 선택.
  - 예: 1·2막 인물 컷 = Higgsfield `nano_banana_2`(백그라운드 에이전트), 3막+피날레 = Magnific `imagen-nano-banana-2`/`seedream-4`(별도 에이전트). 동시 제출 후 일괄 폴링 → 다운로드.
- 각 계정 에이전트의 **저장 경로를 명시**해 혼선 방지. 완료 후 **한 폴더로 통합**하고 30/30 디스크 검증(로그 말고 실제 png).
- ref = 주인공 얼굴 1장 + 제품 목업 1장. 컷 성격에 따라 ref 조합을 다르게(인물=얼굴ref, 제품=제품ref).
- **모델 파라미터 사전 확정:** 생성 전 Higgsfield `models_explore(action='get', model_id=...)` / Magnific `images_models_show`로 resolution 라벨·reference 입력 형식 확인.

### C-2. 영상화 — 재개 가능(resumable) 워커 (대량·장시간 안전)
- 단일 에이전트로 30컷을 한 번에 도는 건 **턴 한도로 깨진다**. → **작업상태 파일**(`videos/seedance/_jobs.json`, cut별 `pending`/`running`(+`job_id`)/`done`)을 두고 라운드 반복:
  1. `running` 잡을 `job_status(sync:true)`로 reap → 완료분 즉시 rawUrl 다운로드 → `done`, **매 변경마다 `_jobs.json` 저장**.
  2. `running < 8`인 동안 `pending` 컷을 업로드 + `generate_video` 제출 → `job_id` 기록(`running`).
  3. 전부 `done`이 아니면 ~20s 후 반복. 라운드/예산 한도면 상태 저장 후 종료 → **메인이 재호출해 이어감**(진행분 보존).
- 이미 제출됐는데 끊긴 잡은 `show_generations`로 회수해 rawUrl만 다운로드(중복 결제 방지).
- 필터/프리셋: nsfw·ip_detected 오탐은 자동 재시도, 프리셋 추천("IN THE DARK" 등)은 `declined_preset_id`로 리터럴 강제. 모든 영상에 `VID_ENHANCE`(→ `03` 참조).

### C-3. 리뷰 콘솔 GATE 17 — 이미지수정 ↔ 영상전환 토글 + 추천 프롬프트 자동
- 리뷰 콘솔 패키지는 **`review_console/`(키트 루트)에 포함** — `python start.py --media-dir <폴더> --mode image|video --backend agent` 원클릭(빌드+서버+워처+브라우저). 사용법은 `review_console/START_HERE.md`.
- 이미지 카드마다 **[이미지 수정 ↔ 영상으로 전환]** 탭. 영상 전환 시 **컷별 추천 영상 프롬프트가 자동 입력**(`--video-prompts <cut→prompt.json>`).
- **`--backend agent`(실가동 필수)**: `worker.py`는 큐(`runtime/revision_queue.jsonl`)만 쌓고, **Claude 에이전트가 MCP(Higgsfield/Magnific)로 실제 재생성**. 기본값 `--backend mock`은 데모 전용.
- ⚠️ 패키지가 `webroot/runtime`을 **공유**한다. 단계 전환 시 **한쪽만 활성**으로 운용.

### C-4. 프리미어 자동 편집 (CEP 파일 브릿지)
브릿지 폴더(`...\Temp\premiere-mcp-bridge\`)에 `command-{id}.json` 작성 → 패널이 실행 후 `response-{id}.json`. ExtendScript는 `return JSON.stringify(...)` 하는 즉시실행함수. (차단 토큰: `eval(` / `new Function(` / `require(` / `__dirname` / `__filename` / "process" / `child_process` — 스크립트에 넣지 말 것. 경로는 포워드슬래시.) 검증된 자동 편집 순서:
1. **정리 임포트**: `root.createBin(name)` → `importFiles(paths,true,bin,false)`로 30컷을 bin에.
2. **풀 어셈블리 시퀀스**: `createNewSequenceFromClips(name, 순서배열, bin)` (배열 순서대로 타임라인 연속 배치).
3. **하이라이트 30초 편집**: 컷마다 `clip.createSubClip(name, startSec, endSec, hard, takeVideo, takeAudio=0)`로 영상-온리 트림 → 서브클립 배열로 `createNewSequenceFromClips('*_30s', subs, bin)`.
4. **오디오 싱크**: `importFiles([vo])` → VO는 `audioTracks[1].overwriteClip(vo, 0)`(A2). **외부 BGM 파일이 있을 경우 조건부**: `importFiles([bgm])` → `audioTracks[0].overwriteClip(bgmSub, 0)`(A1). 내레이션 라인 타임코드에 `seq.markers.createMarker(s)` + `.name`/`.comments`로 싱크 가이드 마커.
5. `app.project.save()`.

> **요약 한 줄:** 비싼 분기는 객관식으로 먼저 확정 → 이미지 Higgsfield+Magnific 2엔진 병렬 → 영상은 resumable 워커 → 리뷰는 GATE 17 콘솔(수정/영상전환) → 프리미어 브릿지로 하이라이트 30초 + (BGM 조건부A1)/VO(A2) 자동 조립. 모든 생성에 `IMG_ENHANCE`/`VID_ENHANCE` 기본 주입.

---

## 부록 D — 미리보기 HTML & 다단계 강화 재생성

### D-1. 자체완결 미리보기 HTML (이미지 · 영상)

**(1) 이미지 스토리보드 미리보기** — `system_v2/_build_*_embed.py` 패턴
- 각 png를 **Pillow로 width 760 리사이즈 → JPEG q80 → base64**로 인라인 임베드 → **HTML 1파일**. 30컷 1.5~1.6MB 수준.
- 카드 구성: 썸네일 + 컷번호 배지 + **막(Act) 배지(색상 매핑)** + 샷/앵글·grade + 한글 장면 + 제품 역할.
- 다크 카드 그리드(`#0b0d12`, 블루 액센트, 16:9 `aspect-ratio`).
- **출력은 반드시 그 버전 폴더 안에** 저장. 버전마다 새 파일(덮어쓰기 금지).

**(2) 영상 미리보기 콘솔** — GATE 17 콘솔의 영상 모드(`<video>` 카드 + 로컬 서버 mp4 서빙). `review_console/`에 포함(`start.py --mode video`).
- 카드가 `<video autoplay muted loop playsinline>` 미리보기. 로컬 서버로 mp4 직접 서빙.

### D-2. 다단계 강화 재생성 (강화를 "여러 번 강조"해서 다시 뽑기)

| 버전 | 주입 상수 | 강조 강도 |
|---|---|---|
| v1 | `COMMON`만 | 기본 |
| **v2** | `COMMON + IMG_ENHANCE` | 정면/아이레벨 배제, 더치·로우·하이, 데마이, 로우키, 매치컷 |
| **v3** | `COMMON + IMG_ENHANCE` (MAX 강조 재주입) | **MAX** — `IMG_ENHANCE`를 한 번 더, 더 강하게: "ZERO front-facing/eye-level", "EVERY single shot", "STRICT low-key", 얼굴 디테일 극대화 문구를 덧붙여 재주입(별도 상수 아님) |

**구현 트릭(프롬프트 재사용):** 새 강화 버전 스크립트에서 기존 JOBS를 `importlib`로 불러와 **강화 상수만 덧붙인다.**
```python
# 별도 상수가 아니라 같은 IMG_ENHANCE 를 MAX 강도로 한 번 더 강조해 재주입
MAX_EMPHASIS = " ZERO front-facing/eye-level on EVERY single shot. STRICT low-key. Maximize facial detail."
JOBS_ALL = [(n, r, p + " " + IMG_ENHANCE + MAX_EMPHASIS) for (n, r, p) in v5.JOBS_ALL]
VERSION  = "v2026-06-03_v3"
```

---

## 부록 E — Splitline "두 계좌의 결투" 세션 총정리 (2026-06-10, v3 표준)

> 핀테크 30초 광고 한 편을 키프레임 200+장·영상 50+편 규모로 제작하며 얻은 시행착오 전부. (#21부터 이어서 번호)

### E-1. 모델 선택 — 처음부터 이걸로 시작하라

> **시행착오 #21 — gpt-image 계열은 인물에 쓰지 않는 이유:** gpt-image-2 계열은 **레퍼런스 얼굴을 왜곡**한다(컷마다 다른 사람). 속도도 느리다. → **인물/얼굴 ref 컷은 무조건 nano_banana_2 계열**: Higgsfield `nano_banana_2`(2k=2752×1536, 4k 가능) / Magnific `imagen-nano-banana-2`(NB Pro, sota·한글 텍스트 최강) / `imagen-nano-banana-2-flash`(NB2, 43초·무인물 대량용). `gpt_image_2`(Higgsfield)는 인물 없는 제품·로고·텍스트 컷에 보조로만.
> **시행착오 #22 — 속도맵:** Magnific 기준 flux-2-klein 5s / grok 9s / **seedream-4 13s(포토리얼 강함, 속도 최우선 시 표준)** / NB2 flash 43s / NB Pro 68s. 동시한도: **Magnific 24(이미지 단위)**, **Higgsfield 계정당 8**.
> **시행착오 #23 — 영상은 HF2(ultra) 전용:** HF1 무료플랜은 Kling 3.0·Seedance 2.0 모두 플랜 게이트. `kling3_0` pro 실출력은 소스 비율을 따라간다 — 시작 이미지를 정확히 1920×1080으로 만들면 1920×1080이 나온다.
> **시행착오 #37 — 멀티패널 캐릭터 레퍼런스 시트(턴어라운드)는 `soul_2`가 아니라 `gpt_image_2`로:** `soul_2`(Higgsfield Soul 2.0)는 `enhance_prompt`가 서버에서 강제 ON이고 끌 수 없다(`enhance_prompt:false`를 보내도 "Higgsfield Soul 2.0 does not support this parameter"로 무시됨) — 그 결과 "TOP ROW 4뷰 + BOTTOM ROW 3뷰" 같은 명시적 멀티패널 구도 지시가 서버에서 임의로 단일 포트레이트 묘사로 재작성되어 통째로 무시된다. 반면 `gpt_image_2`는 프롬프트를 그대로 통과시켜 패널 구조(로우·컬럼·배치)를 지킨다 — 단, #21의 얼굴 왜곡 위험은 여전히 있으므로 패널별 얼굴 일치는 생성 후 직접 확인이 필요.
> **시행착오 #38 — 개별 컷 이미지 모델은 `nano_banana_2`로 통일, `soul_2` 미사용(최종 결정):** `soul_2`는 인물 얼굴 일관성은 좋지만 미디어 첨부가 1장으로 제한되고(`medias` max 1) `enhance_prompt` 강제로 구도 지시를 재작성하는 등 제약이 많다. 운영 단순화를 위해 **개별 컷(인물·제품 불문)은 전부 `nano_banana_2`로 통일**하고, **모든 생성 호출에 해당 레퍼런스 이미지(얼굴 ref·제품 ref, 필요시 둘 다)를 항상 medias로 첨부**한다 — `nano_banana_2`는 멀티 레퍼런스 첨부가 가능해 얼굴+제품을 동시에 걸 수 있다. `soul_2`는 멀티패널 시트가 아예 안 되므로(#37) 더더욱 쓸 이유가 없다. **결론: 개별 컷=`nano_banana_2`(레퍼런스 항상 첨부). `soul_2`는 개별 컷에는 미사용 — 단 #39의 1차 레퍼런스 학습 용도는 예외.**
> **시행착오 #39 — 1차 캐릭터 레퍼런스는 Higgsfield Soul Character 학습으로 전환, `ref/` 폴더로 표준화 + 캐릭터 동결:** 사진 5장 이상이 있으면 `gpt_image_2` 멀티패널 턴어라운드(#37)보다 Higgsfield `show_characters(action:'train')`로 재사용 가능한 Soul Character(`soul_id`)를 학습하는 쪽을 기본값으로 한다 — 사진만 있으면 멀티패널 구도 작성·왜곡 위험(#21) 없이 바로 identity model을 얻는다. **#38의 "개별 컷=soul_2 미사용" 결정과 충돌하지 않는다** — Soul 학습은 1차 얼굴 레퍼런스 스틸(`ref_face.png`)을 `soul_2`로 한 장 뽑는 용도로만 쓰고, 그 스틸을 이후 `nano_banana_2` 컷 생성에 medias로 첨부한다. **저장 위치는 전역 레지스트리(`assets/character_refs/{name}/character.json`, 학습 1회) + 프로젝트별 포인터(`projects/{project}/{version}/ref/{name}_character.json`)로 분리** — `images/ref/`·`keyvisual/` 등 과거 변형 위치는 신규 프로젝트에 쓰지 않고 `ref/`로 통일. **캐릭터 동결:** 동일 인물을 여러 프로젝트에서 쓸 때 `soul_id`를 재학습하지 않고 그대로 재사용한다 — 외형(헤어·의상)이 바뀌어도 인물이 같으면 동일 `soul_id` + 프롬프트로 외형만 조정. 사진이 5장 미만일 때만 #37의 `gpt_image_2` 턴어라운드로 대체.
> **시행착오 #40 — `scenario.md`의 `[duration]`은 편집 길이일 뿐, 생성 길이는 항상 고정값:** `## Cut NN` 마크다운에 적는 `[duration]`(예: 1.0s)은 **최종 조립 시 그 컷을 몇 초로 쓸지**를 가리키는 편집 타임라인 값이다 — 실제 영상 생성(GATE 12 `--duration`)을 그 값으로 바꾸지 않는다. `[duration]`이 고정 생성 길이보다 짧으면 일단 고정 길이 그대로 생성한 뒤 GATE 16 최종 조립에서 필요한 길이만큼 잘라 쓴다. GATE 8에서는 `[duration]` 합계가 목표 광고 길이(보통 30s)와 맞는지만 검증하고, GATE 12의 모델 호출 파라미터에는 영향을 주지 않는다. **연혁:** 2026-06-21 Seedance 2.0 4초→5초 상향 → 2026-06-22(오전) 기본 모델을 Seedance 2.0 → Kling 3.0 Turbo(1080p)로 전환하며 생성 길이를 5초로 고정(사용자 지정) → 2026-06-22(같은 날) "Seedance 2.0 Mini" 신규 런칭에 맞춰 기본 모델을 Kling 3.0 Turbo → Seedance 2.0 Mini(720p·4초)로 재전환(사용자 지정) → **2026-06-22(같은 날, 추가 지정) 백업 체인을 Kling 3.0 Turbo에서 `seedance_2_0`의 `mode` 파라미터만 바꾸는 3단 체인(Mini → 백업1 Fast → 백업2·최종 standard)으로 교체** — Kling 3.0 Turbo는 더 이상 이 영상화 백업 체인에 포함되지 않는다.

### E-2. 인물 컷 문법 — "보도사진" 회피의 핵심

> **시행착오 #24 — 두 얼굴 한 프레임 = 실패:** 와이드 투샷은 얼굴이 작아 보도사진처럼 납작, 두 정체성을 동시에 못 잡아 일관성 붕괴. → **프레임당 얼굴 하나**: 화자만 타이트 CU, 상대는 의상 색만 남은 흐린 등 슬라이버(OTS).
> **시행착오 #25 — 균일조명 시트 ref가 시네마틱을 죽인다:** 의상 고정용 카탈로그 시트를 ref로 걸면 그 조명까지 흡수해 보도사진화. → 시트는 쓰되 프롬프트에 **LOOK OVERRIDE** 강하게: "IGNORE the flat catalog lighting of the reference — relight LOW-KEY with hard golden BACKLIGHT/rim, deep shadows, motivated key."
> **확정 인물 레시피(그대로 복사):** 노을 도시+베네치안 블라인드 배경(밝은 낮·화이트 블로우 금지), 로우키 + 웜 백라이트 림(머리·턱 분리), 더치/로우/하이(정면·아이레벨 0), 데마이 얕은 심도, 서로 마주보는 3/4 시선, 대사 치는 생동 표정, 자연 피부(왁스 금지·모공·비대칭·캐치라이트). **잘 나온 컷 1장을 "레시피"로 선언하고 전 컷 프롬프트에 박는다.**
> **익스트림 앵글 문법(논페이스 확정):** 부감+더치롤 / 웜즈아이+더치롤 / 오버헤드 레이킹 대각 / 로우 스킴(표면 스치기) / 톱다운 매크로 크롭 — 5종 순환이 가장 "TV CF답다"는 사용자 확정.

### E-3. 소품·텍스트·한글

> **시행착오 #26 — 소품 스케일 명시:** "REAL credit-card size (85.6×54mm), correctly scaled to hand/desk — never oversized" 강제.
> **시행착오 #27 — NSFW 오탐 2종:** ① 무인물 제품컷에 얼굴/피부 디테일 보일러플레이트가 붙으면 오탐 → 인물 없는 컷은 **OBJ 전용 블록** 사용(`IMG_ENHANCE_OBJECT`). ② 손 표현은 "a person's hand"로 중립화.
> **시행착오 #28 — 한글 3D 타이포:** NB Pro가 최강이지만 겹자음·문장부호가 깨진다. → ① 글리프 분해 프롬프트("ㄲ = EXACTLY TWO ㄱ strokes") ② 3테이크 뽑아 고르기 ③ **병렬 QA 워크플로우**(검수 에이전트가 이미지를 직접 열어 글리프 판정) 필수.
> **시행착오 #29 — 흰 배경 회귀:** 루마키용 순흑 배경이 간헐적으로 흰 배경으로 나온다. → "On a pure solid black #000000 void background, total darkness edge to edge" + 엣지 픽셀 검증(6점 RGB<10).
> **시행착오 #30 — 크로마키 한글-세이프:** 렌더할 한글을 2~3개 문자열로 제한 + "ALL OTHER UI elements are abstract — no readable or pseudo-readable text"로 가짜 글자 차단.
> **시행착오 #31 — 모델이 못 하는 건 후처리로:** ① 미러 롤 지시 무시 → 투명 PNG를 각도 회전으로 해결. ② 레이저/블레이드 제거는 색 마스크+팽창, 안 되면 "블레이드 없이" 클린 재생성이 정답. ③ 세로쓰기는 "each glyph upright, top-to-bottom" 명시.

### E-4. 루마키·크로마 플레이트 파이프라인 (확정)

1. **순흑 배경 생성**(엣지 검증) → 밝기=알파 루마키 → **풀프레임 유지(오토크롭 금지!** 16:9 캔버스가 깨지면 영상화 때 변칙 해상도 사고**)**.
2. **그린 플레이트**: 하드 매트(밝기 T=36 컷) + 모폴로지 디스펙클(Min/Max 5) + 1.2px 페더 → 순수 #00FF00 합성 → **정확히 1920×1080 정규화**.
3. **크로마 모션 영상 프롬프트(그대로 복사):** "No background music, SFX only. LOCKED-OFF static camera. The pure flat chroma-green background stays COMPLETELY static, uniform and shadow-free for keying — only the subject moves. The subject holds perfectly still for the first 1.5 seconds, then [모션]."
4. **소멸 모션 레퍼토리(검증됨):** 파티클 디졸브 / 블레이드 와이프 / 스플릿 슬라이드 / 글래스 섀터 / 엠버 / 디지털 디레즈 / 리퀴드 리트랙트 / 슬랫 와이프. 등장은 라이트 스윕 / 마이크로 푸시+펄스 / 어셈블-인.

### E-5. 운영 — 속도와 안정성

> **시행착오 #32 — 병렬의 정석:** 컷 순차 처리 금지. **채널(계정)별 서브에이전트가 잡을 전부 먼저 던지고(한도까지) → 일괄 폴링 → 일괄 다운로드.** 진짜 병렬은 서로 다른 풀(Magnific/HF1/HF2)로 — 같은 계정에 에이전트 2개는 한도를 나눠 쓸 뿐이다.
> **시행착오 #33 — 생성은 전부 백그라운드:** 메인은 대화를 유지하고, 생성·폴링·다운로드는 `run_in_background` 에이전트로. 영상 에이전트는 **in_progress 중 턴을 끝내기 쉬움** → "do not end your turn while in_progress, 백그라운드 타이머+until-루프로 페이싱" 명시.
> **시행착오 #34 — API 일시 rate-limit:** 동시 에이전트 3개+에서 발생. → 스태거 시작(30/90/150초) + 호출 실패 시 sleep 45~60 백오프 재시도. 컨텍스트가 비대해진 에이전트(>300k 토큰)는 **새 에이전트로 교체**가 빠르다.
> **시행착오 #35 — 라이브 셀렉 콘솔:** base64 임베드 대신 **상대경로 `<img>` + JS 폴러**(8초마다 미로딩만 캐시버스트 재시도)로 만들면 생성되는 대로 자동 채워진다.
> **시행착오 #36 — 시나리오도 병렬로:** 30초 광고 시나리오는 **워크플로우(3안 병렬 초안 → 심사 → 합성)**가 단일 작성보다 질이 좋다. 12비트 매치컷 체인 + 훅-회수 구조가 "임팩트+즉시 이해"를 동시에 잡았다.

### E-6. 다음 프로젝트 스타트 체크리스트 (이대로 시작)

1. 사진 5장 이상이면 Soul Character 학습(#39, `assets/character_refs/{name}/` + `projects/{project}/{version}/ref/` 포인터, 동일 인물 재사용)으로 1차 얼굴 ref 확보 → 부족하면 gpt_image_2 턴어라운드(#37)로 대체 → **의상 시트·장소 시트** 생성(균일조명) → 시트 ref + **LOOK OVERRIDE 재조명** 조합 확정.
2. 개별 컷=nano_banana_2로 통일(인물·제품 불문, soul_2는 1차 레퍼런스 스틸 생성에만 — #38·#39), 모든 호출에 얼굴·제품 레퍼런스 항상 첨부 / 무인물=NB Pro 또는 seedream-4 / 한글 텍스트=NB Pro+글리프 명시+3테이크+병렬 QA.
3. 매니페스트(json: _blocks+컷별 scene) → 채널별 백그라운드 에이전트 일괄 제출 → 라이브 픽커.
4. 잠금 룩: 노을+블라인드·로우키·백라이트 림·더치/로우/하이·데마이·신용카드 스케일·정면/아이레벨 0.
5. 브랜드 자산: 순흑+엣지검증 → 루마키(풀프레임) → 그린 1920×1080 → HF2 Kling/Seedance 모션.
6. 모든 수정은 새 버전 폴더, 모든 한국어 산출물은 UTF-8 BOM.

---

## 부록 F — ARDENMOOR(가상 싱글몰트 위스키) 세션 비주얼·카메라 디렉션 (2026-06-13)

> 제품/환경 광고(인물 얼굴 없음, 손·실루엣만)에서 사용자가 반복·강조한 이미지 생성/수정 요청을 박제한 규칙. 강화 상수 풀텍스트(`IMG_ENHANCE_OBJECT`)는 `03_reference_enhance-prompts.md` 참조.

### F-1. 화각·구도 (FOV & COMPOSITION) — "뻔한 아이레벨은 절대 금지"

- **정면·아이레벨 전면 금지.** 모든 컷은 **익스트림 로우 / 익스트림 하이(탑다운 부감) / 더치(20~40° 롤)** 중 하나.
- **★진짜 로우앵글의 정의:** "카메라를 바닥에 붙이고 피사체를 가파르게 올려다보는(웜즈아이) 앙각". 프롬프트에 `camera resting on the floor, tilted steeply UPWARD, subject looms overhead, dramatic upward foreshortening, converging verticals, seen from BELOW`를 명시.
- **렌즈에 따른 분기:**
  - 광각이면 → `wide-angle cine lens with visible barrel distortion`.
  - 망원이면 → `telephoto compression, ULTRA-shallow depth of field, razor-thin plane of focus, creamy bokeh`.
- **매크로 인서트는 극히 얕은 심도:** `macro lens wide open (f/1.4), razor-thin focus, sumptuous creamy bokeh, only one point sharp`.

### F-2. 조명·룩 / F-3. 카메라 바디·렌즈 룩 / F-4. 오디오 / F-5. 모션 / F-6. 제품·일관성

- **조명:** 단일 하드 백라이트 + 네거티브 필. 플랫 정면 필 금지, 하이키 금지, 로우키 럭스만.
- **카메라 룩:** ARRI Alexa 65 + 빈티지 아나모픽. NOT clinical digital sharpness — 부드러운 필믹 그레인(Vision3 500T), Black Pro-Mist.
- **오디오:** 모든 영상 프롬프트 맨 앞 = SFX only, NO BGM.
- **모션:** FPV 다이브·더치·고속 오빗·스피드램프·매크로 돌진·휙팬. "끊임없이 전진하는 속도감 + 미세 디테일 속으로 파고드는 매크로 탐험".
- **제품 일관성:** 제품 형태 절대 고정. 등장 컷은 확정 제품 이미지를 product/image 레퍼런스로 동봉.

> **IMG_ENHANCE_OBJECT 풀텍스트(F-7):** `03_reference_enhance-prompts.md` 참조.

---

## 부록 G — STAGELIGHT 세션 이미지 디렉션 로그 & 인물 강화 상수 (2026-06-13)

> 강화 상수 풀텍스트(`IMG_ENHANCE_PERSON`)는 `03_reference_enhance-prompts.md` 참조.

### G-1~G-4. 핵심 규칙 요약

- **화각:** 아이레벨 정직 구도 절대 금지. 더치 / 하이 / 로우 중 하나. 광각=배럴/피쉬아이 왜곡, 망원=초얕은 심도+보케.
- **조명:** 네거티브 필 역광. 로우키 only. 컬러 컨트라스트/밸런스(마젠타 #FF1F8E × 시안 #00E8FF).
- **카메라 룩:** ARRI Alexa(65) + 빈티지 아나모픽. 선예도 지양 → 부드러운 시네마틱 + 고급 35mm 그레인(Vision3 500T). 절대 금지: CGI/3D 렌더/게임/일러스트.
- **인물·브랜드 일관성:** 주인공 얼굴 ref 락(IDENTITY LOCK). 의상 = 세련된 테일러드 차콜 코트 + 블랙 크루넥. 제3자 브랜드 로고·읽히는 간판 텍스트 금지.

### G-6. 컷별 수정 요청 로그 (시간순 — 무엇이 NG였고 어떻게 고쳤나)
| 라운드 | 사용자 수정 요청 요지 |
|---|---|
| v1→v2 | "싸구려·AI틱·중국 이미지 같다, 5단계 고도화." 텍스트 전면 삭제. ARRI 저채도+할리우드 그레인. 실사·세련 주인공. nano-banana 2엔진 비교 선택. |
| 주인공 | 링크 인물의 얼굴 CU만 REF, 의상은 컨셉 맞춰 변경. |
| 로고 | 스포티파이식 심플 텍스트 워드마크 5안 → L1(소문자 마젠타) 확정. |
| v3 | "더 다이내믹·예술성·심미성." 익스트림 매크로 / 익스트림 하이앵글 / 데마이 / 역광 / 조명 심미 극대화. |
| v4 | "30컷 더, 즉시 TV-CF급." 할리우드 마스터 조명(네거티브 필·모티베이티드·볼류메트릭 라이트샤프트). |
| v5 | 전체 재생성 90장(30씬×3안). 알렉사 바디+렌즈, 선예도보다 부드러운 시네마틱 그레인. 아이레벨 금지. |

> **IMG_ENHANCE_PERSON 풀텍스트(G-5):** `03_reference_enhance-prompts.md` 참조.

---

## 부록 H — STAGELIGHT 세션 영상화 로그 & 운영 정답 (2026-06-13)

> 강화 상수 풀텍스트(`VID_ENHANCE_SFX`)는 `03_reference_enhance-prompts.md` 참조.

### H-1. 절대 오디오 규칙 (그 무엇보다 우선)
- **모든 영상 = 효과음(SFX)만, BGM/음악/노래 절대 없음.** 프롬프트 **맨 앞 최우선 라인**으로 박는다. STAGELIGHT가 음악앱이어도 *생성 클립 자체*는 SFX only. 음악은 생성 밖(편집)에서만.

### H-3. 엔진·설정
| 항목 | 값 |
|---|---|
| MODEL | `seedance_2_0` (Higgsfield) |
| 길이/해상도/비율 | 4초 · **1080p** · 16:9 · mode `std` |
| 입력 | **start_image** = 확정 키프레임 I2V |
| 오디오 | generate_audio 파라미터 없음 → 프롬프트 SFX 지시로 디제틱 사운드 |
| 비용 | **1클립 = 36 크레딧** (4초 1080p). `get_cost:true`로 프리플라이트 |
| 병렬 | **Higgsfield 2계정 병렬** + 계정당 **8 동시** 한도 |

### H-4. 업로드·소스 처리
- **magnific 2K(예: 2752×1536, 5~7MB)는 업로드 한도(≤4MB) 초과** → 업로드 전 **1080p(1920폭) jpg q92로 다운스케일**.
- 업로드: `media_upload(filename)` → presigned URL에 **curl PUT --data-binary** → `media_confirm` → media_id.
- **media_id TTL ≈ 15분** — 업로드 직후 곧바로 제출.

### H-5. 에러·복구
- **프리셋 추천 차단** → `declined_preset_id` 동봉해 리터럴 강제.
- **ip_detected / nsfw 오탐**, **`fetch failed`** → 해당 컷만 1~2회 재시도.
- **job_id 분실** → `show_generations`로 회수해 rawUrl만 다운로드.
- **MCP 계정 연결 끊김** → 연결된 다른 Higgsfield 계정으로 우회 재렌더.

### H-7. 컷 유형별 카메라 무브 매핑 (검증된 기본값)
| 컷 유형 | 무브 |
|---|---|
| 오프닝/도시 다이브 | 초광각 FPV 전진 다이브 + 35~60° 뱅킹 더치 롤 → 어두운 구멍 스피드램프 |
| 제품/스카이라인 히어로 | 극로우 크레인업 + 슬로 오빗(수직 수렴) |
| 매크로 파츠/링 타이포 | 락드센터 오빗 / 매크로 푸시 |
| 소재 X-ray 모핑 | 오빗 + 네거티브플래시 스피드램프 → 스매시컷 |
| 인물 워크인 | 더치 45° 핸드헬드 워크인 → 임팩트 휙팬 |
| 스트리트 POV | 핸드헬드 피쉬아이, 손이 렌즈 덮으며 컷 |
| 라이트 트레일 | 망원 휙팬 + 스피드램프 |
| 글자 터널 | 1점투시 돌리인 → 화이트아웃 |
| 카이도스코프/광장 | 펄스줌 스핀 / 오버헤드 크레인 회전 보텍스 |
| 매크로 인서트 | 슬로 푸시인 + 랙포커스(데마이) |
| 드롭 버스트 | 휙팬/스핀 0.x 버스트 + 서브프레임 스터터 |
| 클라이맥스 | 로우 크래시줌 + 아크 |
| 로고 락업 | 매우 느린 푸시인, 백키 플레어 점등 |

---

## 부록 I — ARDENMOOR 세션 영상(Seedance) 생성·수정 디렉션 (2026-06-13, 제품·오브제·매크로)

> 강화 상수 풀텍스트(`VID_ENHANCE_OBJECT`)는 `03_reference_enhance-prompts.md` 참조.

### I-1. ⛔ 오디오 — 최우선
- **모든 영상 = bgm 없고 효과음만, 맨 앞에 가장 강조.** `AUDIO (TOP PRIORITY): diegetic SFX ONLY — absolutely NO background music, NO BGM, NO musical score.`

### I-2. 카메라 무브 — "끊임없이 빠른 전진 + 매크로 탐험 + 컷 연결"
```text
Relentless high-speed forward FPV/macro push, continuously accelerating, heavy motion-blur streaks, diving deeper into micro-detail, ending as the surface/light/texture fills and SWALLOWS the frame (match-cut out-point into the next cut).
```
- **스피드램프:** `begin in crisp slow motion … then SNAP into a fast forward push … then ramp back to slow as it flares.`

### I-3. 엔진·설정
- model `seedance_2_0` / 16:9 / duration 4 / **resolution 반드시 "1080p" 명시** — ★서버B는 해상도 누락 시 720p로 떨어짐(실측). I2V(start_image=확정 이미지 1792×1008).

### I-4. 콘텐츠 필터 우회
- **프리셋 추천 차단:** `declined_preset_id` 동봉해 리터럴 강제(모든 영상 호출 기본 권장).
- **nsfw/ip_detected 오탐**: ① 표현 순화 ② start_image를 다른 엔진/버전으로 교체 ③ 다른 계정 재시도.

### I-6. 컷 유형별 무브 매핑 (ARDENMOOR 실측)
| 컷 유형 | 무브 |
|---|---|
| 외관/창고 | 초광각 FPV 상승·전진 다이브 + 더치 롤 → 안개·구멍 흡수 |
| 매치컷(배럴→병) | 번홀 블랙홀 돌진 / 랙포커스 더치 피벗 / 소실점 FPV / 포어 휙팬 / 병기둥 상승 |
| 제품 리빌 | 슬로 dolly-in + 아크 오빗 + 라이트 스윕(라벨 금박 점등) |
| 매크로 인서트 | 고속 오빗 / 탑다운 돌진 / 스피드램프 / 크라운 돌진+슬로모 스냅 / 라이트 스윕 / 균열 속 돌진 / 레그 추적 |
| 스피드램프 디테일 | 슬로모 시작 → 고속 매크로 스냅 → 슬로 플레어 |

> **요약:** SFX-only 맨 앞 → 끊임없는 전진 FPV·매크로 다이브 + 스피드램프(`VID_ENHANCE_OBJECT`, → `03` 참조) → 1080p 명시·declined_preset 동봉 → 2계정 백그라운드 분담.

---

## 용어 사전

- **img2img**: 참조 이미지를 넣고 생성해 그 얼굴/제품 모양을 유지하는 방식.
- **데마이(얕은 심도, shallow depth of field)**: 초점 맞은 곳만 또렷하고 배경은 보케로 흐려지는 망원 클로즈업 느낌.
- **보케(bokeh)**: 초점이 안 맞아 동그랗게 번지는 배경 흐림.
- **매치컷(match cut)**: 앞 컷의 형태·동작을 다음 컷이 닮은 형태로 이어받아 부드럽게 넘어가는 편집.
- **그레이드(color grade)**: 영상 전체의 색 분위기(예: 차가운 블루, 따뜻한 골든).
- **림라이트/역광(rim/back light)**: 인물 뒤에서 비춰 윤곽을 빛나게 해 배경과 분리하는 조명.
- **데드 스페이스(dead space)**: 의미 없이 비어 보이는 화면 공간(피해야 함).
- **네거티브 스페이스(negative space)**: 의도적으로 비운 여백(로고 자리 등).
- **피날레/히어로샷**: 광고 끝의 제품 단독 클로즈업·매크로 컷.
- **payoff**: 쌓아온 감정이 터지는 보상 순간(재회·성취 등).
- **start_image**: image-to-video에서 영상의 첫 프레임으로 쓰는 입력 이미지. Seedance medias의 role.
- **루마키(luma key)**: 밝기를 기준으로 어두운 부분을 투명하게 빼는 처리.
- **오토크롭(autocrop)**: 투명/여백을 뺀 내용물 바운딩박스로 이미지를 잘라내는 것.
- **8-동시 한도(concurrency cap)**: 한 계정이 동시에 돌릴 수 있는 생성 작업 수 제한(Higgsfield=8).
- **프리셋 추천(preset recommendation)**: Higgsfield가 프롬프트를 보고 자사 프리셋을 권하며 일반 생성을 막는 안내. `declined_preset_id`로 거절하고 리터럴 생성.
- **voice_settings(stability/style)**: ElevenLabs 음색 제어. stability↑=일정·차분, style↑=표현 과장.
- **데마이**: 현장 은어로 쓰는 **얕은 심도(보케) 클로즈업**을 가리킴(이 문서 한정 표기).
- **리뷰 콘솔(review console)**: 생성물(이미지/영상)을 카드 그리드로 띄워 선택→수정요청→Enter로 즉시 재생성하는 자동 팝업 HTML(GATE 17).
- **브리지 큐(bridge queue)**: 샌드박스된 HTML이 MCP를 직접 못 부르므로, 로컬 서버가 요청을 `revision_queue.jsonl`에 적고 에이전트가 그걸 읽어 처리하는 중계 방식.
- **nano_banana_2**: Higgsfield의 고품질 이미지 모델(4K·텍스트 강점). 인물 ref 컷 기본 모델. (대안 `gpt_image_2`)
- **seedance_2_0** ("Seedance 2.0" / 웹 UI "Seedance 2.0 Mini"·"Seedance 2.0 Fast"·"Seedance 2.0" 프리셋 전부 같은 job id): Higgsfield의 영상 생성 모델(job id `seedance_2_0`, Bytedance). 입력은 `medias`의 `image`/`start_image`/`end_image`/`video`/`audio` role. `resolution`은 `480p`/`720p`/`1080p` 중 선택(기본·이 플레이북 모두 720p), `duration`은 4~15초 범위(모델 기본 5, 이 플레이북은 4초 고정), `mode`는 `std`(기본, 고품질)/`fast`(저렴·1080p 미지원), `generate_audio`는 **기본 true**라 No-BGM 규칙을 지키려면 매 호출 `false`로 명시해야 한다. `aspect_ratio`는 `16:9`/`9:16`/`1:1`/`4:3`/`3:4`/`21:9`/`auto`. 2026-06-22 영상 기본 모델(720p·4초, 사용자 지정). **3단 백업 체인(전부 이 model_id, `mode`만 다름):** ① "Mini"(카탈로그에서 별도 model_id가 확인된 경우에만 그걸로 호출) → ② **Mini가 카탈로그에 안 잡히면 바로** 백업1 `mode:'fast'`("Fast") → ③ Fast도 안 될 때만 백업2·최종 `mode:'std'`("standard"). ⚠️ "Seedance 2.0 Mini"는 2026-06-22 Higgsfield 웹 UI에 EXCLUSIVE로 별도 노출됐으나 CLI/MCP 카탈로그에는 별도 model_id로 아직 안 잡힘 — **Mini 미확인을 std로 대신 채우지 않는다**, 미확인이면 곧장 백업1(Fast)로 간다. Kling 3.0 Turbo는 이 백업 체인에서 제외됨(2026-06-22).
- **kling3_0_turbo** ("Kling 3.0 Turbo"): Higgsfield의 영상 생성 모델(job id `kling3_0_turbo`). 입력은 `medias`의 `start_image` role 1장(텍스트만으로도 생성 가능). `--resolution`은 `720p`/`1080p` 중 선택(모델 기본 720p), `--duration`은 3~15초 범위(이 플레이북은 5초 고정). `--aspect_ratio`는 `16:9`/`9:16`/`1:1`. 2026-06-22 오전 한때 영상 기본 모델이었으나 같은 날 `seedance_2_0`("Mini")로 대체됐고, 이어서 백업 체인에서도 제외됨(백업은 `seedance_2_0`의 `mode:'fast'`→`mode:'std'`로 전환) — 더 이상 이 영상화 흐름에서 쓰이지 않는다.
- **declined_preset_id**: Higgsfield가 프리셋 추천으로 생성을 막을 때, 같은 params에 추천된 preset id를 넣어 리터럴 생성을 강제하는 파라미터.
