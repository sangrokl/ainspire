# 00_core.md — 광고 스토리보드 플레이북 v2 (진입점·라우터 + 필수 규칙)

> **이미지·영상 생성은 Higgsfield(MCP 또는 CLI) · Magnific MCP. 내레이션은 ElevenLabs MCP(기본) · Higgsfield TTS(백업1) · ElevenLabs 직접 API(백업2). BGM은 Suno 프롬프트 제안(GATE 13) → 사용자 직접 생성.**

---

## 이 문서의 목적

광고 영상 한 편을 **기획 → 스토리보드(이미지) → 영상화 → 내레이션(VO) → 로고 → 최종 완성본 조립**까지, 기초 지식이 전혀 없는 사람도 객관식 질문에 답하기만 하면 끝까지 만들 수 있게 만든 단계별 진행 대본이다.  
AETHER(에너지드링크)·HALO(스마트워치) 광고를 컨셉 v1→v10까지 수없이 갈아엎고, 영상·내레이션·로고까지 실제로 뽑아내며 얻은 시행착오를 그대로 녹였다.

> **이 문서를 쓰는 에이전트에게(IMPORTANT):**
> 1. 각 **GATE(관문)**에 도착하면, 그 GATE의 질문을 `AskUserQuestion` 도구로 **객관식**으로 물어라. 사용자가 전문용어를 몰라도 고를 수 있게 옵션마다 쉬운 설명을 붙여라.
> 2. 사용자가 답하기 전에는 다음 GATE로 넘어가지 마라. 비싼 이미지 생성(돈·시간)이 걸린 분기는 특히 먼저 묻는다.
> 3. 모든 답을 모으면 `기획안(PROJECT_BRIEF)`을 먼저 텍스트로 정리해 보여주고 승인받은 뒤, 생성으로 넘어간다.
> 4. 용어가 처음 나오면 한 줄로 풀어 설명한다. (04_reference_lessons-appendix.md 맨 끝 [용어 사전] 참고)
> 5. **`AskUserQuestion` 호출 규칙 (자주 나는 실수 방지):** 설명 문장만 써 놓고 도구를 빈 채로 부르지 마라. **한 번의 호출에 `questions` 배열을 반드시 채워서** 보낸다 — 질문마다 `question`(질문문)·`header`(짧은 라벨)·`options`(2~4개, 각 `label`+`description`) 가 전부 있어야 한다. 안내·설명은 별도 문장이 아니라 **질문/옵션 텍스트 안에** 녹여라. (`questions` 누락 시 `InputValidationError: questions is missing`로 호출이 실패하고 GATE가 멈춘다.) 한 번에 최대 4개 질문까지.
> 6. **한글 깨짐 방지 — `header`·`label` 필드 규칙:** `header`는 chip UI에서 한글이 깨질 수 있으므로 **반드시 영어 1~2단어**로 쓴다 (예: `"Brand Tone"`, `"Ad Style"`, `"Protagonist"`, `"Structure"`). `label`(선택지 이름)은 한글 가능하나 **4어절 이내**로 짧게 쓴다. `question`과 `description`은 한글로 자유롭게 작성해도 무방하다.

---

## ★ 로딩 가이드 — 이 플레이북 어떻게 읽나

에이전트는 항상 이 파일(`00_core.md`)을 **먼저** 읽는다(필수 규칙 = 규칙 0·절대 규칙·강화 프롬프트가 여기 풀텍스트로 들어 있다). 그 다음은 단계·유형에 따라 온디맨드로 로드한다.

| 상황 | 읽을 파일 |
|---|---|
| **시작 직후 (1회 필수)** | `04_reference_lessons-appendix.md`의 **부록 E 섹션만** — v3 표준 확정 정답(모델 선택·단독 얼굴 CU·시트 재조명·한글 QA·루마키/크로마·병렬 운영). 규칙 6과 동일. |
| **기획 단계(G1~G11)** | `01_planning_G1-G11.md` |
| **제작 단계(G12~G17)** | `02_production_G12-G17.md` |
| **이미지·영상 생성 직전** | 공통 필수(규칙0·`IMG_ENHANCE`·`VID_ENHANCE`)는 **이 파일 아래**. 유형별 확장 상수(PERSON/OBJECT/SFX)는 `03_reference_enhance-prompts.md` |
| **그 외 에러·세션 노하우·부록 F~I·용어** | `04_reference_lessons-appendix.md` (필요 시 온디맨드) |

### 프로젝트 유형별 상수 선택 (생성 직전)

| 유형 | 이미지 | 영상 |
|---|---|---|
| **인물 광고** (주인공 얼굴 등장) | `IMG_ENHANCE` + `IMG_ENHANCE_PERSON`(03) | `VID_ENHANCE` + `VID_ENHANCE_SFX`(03) |
| **제품·오브제 광고** (인물 얼굴 없음) | `IMG_ENHANCE` + `IMG_ENHANCE_OBJECT`(03) | `VID_ENHANCE` + `VID_ENHANCE_OBJECT`(03) |
| **공통 기본** (모든 컷 공통) | `IMG_ENHANCE` (아래) | `VID_ENHANCE` (아래) |

> 이 가이드가 "필수 규칙 항상 읽기 + 단계·유형별 온디맨드 로딩"의 핵심이다.

---

## 우리가 만드는 것 (최종 산출물 체인)

1. **스토리보드**: 30컷 내외 정지 이미지 + 한눈에 보는 HTML. *(생성 2단계: ① gpt_image_2로 30컷 일괄 프리뷰 → 승인 → ② 컷마다 최종 1장 생성)*
2. **영상**: 각 컷을 image-to-video로 움직이는 4초 클립으로 (컷당 1개).
3. **BGM**: 30초 광고 음악 — 에이전트가 Suno 프롬프트를 제안, 사용자가 [suno.com](https://suno.com)에서 직접 생성.
4. **내레이션(VO)**: 영문 보이스오버 (ElevenLabs MCP `text_to_speech` — 기본, 이 환경에 연결되어 있으면 별도 키 불필요. 백업: Higgsfield TTS `inworld_text_to_speech` / ElevenLabs 직접 API).
5. **로고**: 투명 PNG (엔딩 합성용).
6. **최종 완성 스토리보드**: 기획안 + 타임코드별 내레이션 + 컷별 영상 키프레임을 합친 보기 좋은 HTML 한 파일.

> **BGM은 API로 자동생성하지 않는다** — GATE 13에서 Suno 프롬프트만 제안하고, 사용자가 직접 Suno에서 생성해 후반 조립(GATE 16/부록 C-4)에서 얹는다.

---

## 쓰는 도구 (v2 기준)

| 단계 | 도구 | 실행 경로 |
|---|---|---|
| **이미지 생성** | **Higgsfield CLI / MCP · Magnific MCP** | CLI `higgsfield generate create gpt_image_2 …` · MCP `generate_image` · Magnific `images_generate` (아래 [생성 엔진] 참조) |
| 스토리보드 HTML | Python + Pillow (base64 embed) | `system_v2/_build_*_embed.py` |
| **영상화** | **Higgsfield CLI / MCP(seedance_2_0) · Magnific MCP** | CLI `higgsfield generate create seedance_2_0 … --start-image` · MCP `generate_video` · Magnific `video_generate` |
| **업스케일·누끼** | **Magnific MCP** | `images_upscale` / `images_remove_background` |
| **내레이션 TTS** | **ElevenLabs MCP(`text_to_speech`)** | MCP `text_to_speech` (이 환경에 연결되어 있으면 별도 키 불필요) · 백업1 Higgsfield TTS — CLI `higgsfield generate create inworld_text_to_speech` · MCP `generate_audio` · 백업2 ElevenLabs 직접 API `system_v2/_gen_*_vo.py`(ELEVENLABS_API_KEY 필요) |
| **로고 투명화** | Pillow 루마키 / Magnific `images_remove_background` | `system_v2/_logo_transparent.py` 패턴 |
| 폴링·다운로드(영상) | **CLI `--wait` 또는 백그라운드 에이전트** | CLI는 `--wait`가 폴링 처리(토큰 0) · MCP는 `Agent(run_in_background)` |

### 🔌 STEP 0 — 생성 엔진 연결 확인 (제일 먼저, 생성 전 필수)
이미지·영상은 생성 엔진(Higgsfield CLI/MCP 또는 Magnific MCP)으로 만든다. **작업을 시작하면 가장 먼저 연결을 확인하고, 안 되어 있으면 연결부터 끝낸 뒤 진행한다. 셋 중 최소 하나면 된다.**
1. **확인:** Higgsfield CLI `higgsfield account status`(로그인·잔액) / Higgsfield MCP `balance` / Magnific `account_balance` — 정상 응답이면 연결됨.
2. **인증만 안 됨(설치/서버는 있음):** CLI `higgsfield auth login`(브라우저 OAuth) / Higgsfield MCP `authenticate`→로그인→`complete_authentication` / Magnific 첫 호출 시 브라우저 OAuth.
3. **설치/서버 자체가 없음:** Higgsfield MCP 서버 없으면 데스크톱 앱 로그인 후 클라이언트 연결 / Magnific은 클라이언트 MCP 설정에 `https://mcp.magnific.com`(streamable HTTP) 추가 → OAuth(이 둘은 사용자에게 요청). **Higgsfield CLI는 선택** — 쓰려는데 미설치면 아래 [생성 엔진]의 [CLI 설치 안내] 3단계를 사용자에게 전달.
4. **MCP 하나라도 연결되면 생성 단계로 갈 수 있다(CLI 없이도 OK).** 여러 개면 병렬·역할 분담(단발=MCP, 일괄=CLI가 편함). **내레이션 = ElevenLabs MCP(`text_to_speech`)가 기본** — 이 환경에 연결되어 있으면 OK, 별도 키·`.env` 불필요. *(백업1: Higgsfield TTS(`inworld_text_to_speech`) — Higgsfield 연결만 있으면 OK. 백업2: ElevenLabs 직접 API 쓰려면 `system_v2/.env`의 `ELEVENLABS_API_KEY`도 확인 — `node system_v2/check_api_connections.mjs`.)* **연결 전까지 생성 단계로 가지 마라.**

---

## 생성 엔진 (Higgsfield CLI · Higgsfield MCP · Magnific MCP)

> 이미지·영상 생성 경로는 **3가지**(전부 OAuth, 키 관리 없음 — 내레이션은 ElevenLabs MCP 기본(키 불필요), ElevenLabs 직접 API 백업 경로만 키 필요). **우열·강제 없다. 연결된 걸 쓰면 된다.** 같은 컷을 여러 경로로 뽑아 베스트를 고르는 병렬도 가능.
>
> **특성 참고 (어느 것도 필수가 아님):**
> - **Higgsfield MCP** — 기본 경로. 도구 호출이라 세션 안에서 결과가 바로 뜬다. 단발·인터랙티브 확인에 편하고, **이것만으로 전 과정이 가능**하다.
> - **Higgsfield CLI** *(선택 — 깔려 있으면 써도 된다)* — 일괄·무인 배치에 편하다(`--wait`가 폴링 처리 → 토큰 절약, `--json` 배치). 결과는 URL 반환 → 저장은 다운로드 한 단계. **미설치면 아래 [CLI 설치 안내]를 사용자에게 전달**(설치는 선택).
> - **Magnific MCP** *(선택)* — 업스케일·누끼·캐릭터 학습(Soul)·TTS 전용 툴 보유.

| | Higgsfield CLI | Higgsfield MCP | Magnific MCP |
|---|---|---|---|
| 인증 | `higgsfield auth login` (OAuth) | 데스크톱 앱 OAuth | `https://mcp.magnific.com` OAuth |
| 호출 | 셸 `higgsfield generate create <model> …` | 도구 `generate_image`/`generate_video` | 도구 `images_generate`/`video_generate` |
| 이미지 모델 | `gpt_image_2`·`nano_banana_2`·`seedream_v4_5` … (`model list --image`) | `nano_banana_2`/`gpt_image_2` | `imagen-nano-banana-2`(NB Pro)·`seedream-4` (`images_models_list`) |
| 영상 모델 | `seedance_2_0`·`kling3_0`·`veo3_1` … (`model list --video`) | `seedance_2_0` | (`video_models_list`) |
| 레퍼런스 | `--image`/`--start-image`/`--end-image`/`--audio` = 로컬경로(자동 업로드) **또는 이전 job ID** | `media_upload`→`media_confirm` → `medias:[{role,value}]` | `creations_*_upload` 또는 reference 입력 |
| 폴링/대기 | `--wait`(토큰 0, `--wait-timeout 20m`) | job_id 폴링(토큰 소모) | `creation_status`/`creations_wait` |
| 캐릭터 일관성 | `soul-id create` → `--soul-id`, 또는 job-ID ref 재사용 | `media_upload`+generation_id 재사용 | `custom_references_create`(Soul) |
| 비용 견적 | `generate cost <model> …` (생성 전) | — | — |
| 크레딧 | `account status` | `balance` | `account_balance` |
| 보너스 | `--json` 배치·크로스 에이전트 | 계정당 8-동시 한도 | 업스케일·누끼·TTS·Soul 학습 |

### CLI 핵심 명령 (생성 단계 — 전부 4종+프리뷰 승인 후 호출)
```bash
# 이미지 1컷
higgsfield generate create gpt_image_2 --prompt "<규칙0[A] + IMG_ENHANCE + 장면>" --aspect_ratio 16:9 --resolution 2k --wait
# 인물 일관성: 개별 컷은 nano_banana_2로 통일, 얼굴·제품 레퍼런스 이미지를 매 호출에 첨부 (부록 E #38 — soul_2 미사용)
higgsfield generate create nano_banana_2 --prompt "<규칙0[A] + IMG_ENHANCE_PERSON + 장면>" --image ref_face.png --image ref_product.png --aspect_ratio 16:9 --resolution 2k --wait
# 영상화: 확정 이미지(job ID 또는 경로)를 first frame으로
higgsfield generate create seedance_2_0 --prompt "<규칙0[B] No-BGM + VID_ENHANCE + 모션>" --start-image <이미지_jobID_또는_경로> --duration 5 --wait
# [1단계] 30컷 일괄 프리뷰 (gpt_image_2 — 구성 확인용, 승인 전)
# 셸 루프로 컷별 create --wait, 또는 --json 으로 job ID만 받고 나중에 generate wait
# [2단계] 승인 후 — 컷마다 최종 1장 생성 (모델·해상도는 G8 승인 사양 그대로)
```
> **결과 저장(CLI):** CLI는 결과 **URL을 반환**한다 → `projects/{project}/{version}/images|videos/…`에 쌓으려면 URL 다운로드(PowerShell `Invoke-WebRequest -OutFile`, mac/linux `curl -o`) 한 단계를 붙인다. (MCP 경로는 도구가 경로/URL을 함께 반환.)
> **엔진 선택 디테일:** 인물 일관성·시리즈 = nano_banana_2 계열(셋 다 보유). 한글 텍스트·포토리얼 = Magnific NB Pro/seedream. 업스케일·누끼·캐릭터학습·TTS = Magnific 전용. 세부 속도·동시한도 맵은 `04_reference_lessons-appendix.md` 부록 E.
> **`gpt_image_2` 프롬프트 작성:** `--prompt` 본문은 `gpt-image-prompt` 스킬(Scene/Subject/Important details/Use case/Constraints 5단 구조 + 안티슬롭 규칙 — "stunning" 대신 구체적 시각 정보, 텍스트는 따옴표+폰트 명시)을 적용해 작성한다. 단, 규칙 0[A]·`IMG_ENHANCE`(아래)가 더 상위 — 충돌 시 규칙 0이 이긴다. (인물/얼굴 ref 컷에는 여전히 쓰지 않음 — 부록 E #21.)
> **공통 규칙(경로 무관 동일):** 규칙0 프리픽스 + ENHANCE 상수 주입(`03`), 상표는 디자인 언어로, 결과는 새 버전 폴더 저장(덮어쓰기 금지).

### CLI 설치 안내 (선택 — CLI를 쓰려는데 미설치일 때 사용자에게 그대로 전달)
> CLI는 **필수가 아니다** — MCP만으로 전 과정이 된다. 사용자가 CLI를 쓰고 싶은데 안 깔려 있으면 아래 3단계를 그대로 안내한다. 인증·업로드·폴링을 CLI가 알아서 처리한다.
> 1. **설치** — `npm install -g @higgsfield/cli` *(한 줄. auth·업로드·폴링 자동)*
> 2. **로그인** — `higgsfield auth login` *(브라우저가 열리고 5초, OAuth)*
> 3. **(선택) 에이전트에 스킬 연결** — `npx skills add higgsfield-ai/skills` *(Claude Code·Cursor·Codex 등 12+ 에이전트 지원 → 이후 "Higgsfield로 이미지 만들어줘" 한마디로 호출)*

---

## ⛔ 규칙 0 — 이미지·영상 생성 시 무조건·강제 (NON-NEGOTIABLE, 어떤 컷도 예외 없음)

> **이 블록은 이 문서를 실행하는 모든 에이전트에 대한 최우선 강제 지시다. 아래 두 프리픽스를 빼먹은 생성은 즉시 폐기·재생성한다. 프롬프트 프리뷰 테이블에 "MANDATORY 프리픽스 주입됨"을 반드시 표기한다.** (출처: Splitline 세션 — 사용자가 매 컷 반복 요청한 항목.)

**[A] 이미지 — 모든 이미지 프롬프트에 아래를 반드시 합친다 (화각·구도·네거티브 필·역광 강제):**
```text
MANDATORY IMAGE PREFIX (append to EVERY image prompt, no exceptions):
— 화각/구도(FOV & COMPOSITION): ZERO front-facing, ZERO eye-level. The subject NEVER looks into the lens. Use ONLY low-angle, high-angle or dutch-angle framing; off-center rule-of-thirds; telephoto shallow-DOF (demai) with clear 3-layer FG/MG/BG depth separation. People = ONE dominant face in tight CU / OTS (the other person only a blurred wardrobe-colored back-sliver) — never a flat two-shot.
— 역광/림라이트(BACKLIGHT): hard warm BACKLIGHT / rim-light from behind that traces the subject's silhouette and separates it from the background. Motivated key from a window/blinds. NO flat frontal fill light.
— 네거티브 필(NEGATIVE FILL): place black negative fill on the shadow side — let one side of the face/object fall into deep controlled shadow; sculpt the form, raise contrast, kill flat ambient. LOW-KEY only, NEVER high-key, no blown highlights.
```

**[B] 영상 — 모든 영상 프롬프트의 맨 앞에 아래를 반드시 둔다 (BGM 절대 금지 · 효과음만):**
```text
MANDATORY VIDEO PREFIX (must be the FIRST line of EVERY video prompt, no exceptions):
No background music. NO BGM. NO score. SFX only — at most a few subtle diegetic sound effects (footsteps, taps, cloth, clicks). The track carries NO musical bed whatsoever. (BGM/내레이션은 전부 후반 합성으로만 올린다.)
```

> 위 [A][B]는 아래 `IMG_ENHANCE`·`VID_ENHANCE`(규칙 5)보다 **상위**다. 충돌 시 규칙 0이 이긴다.

### 절대 규칙 5가지 (어기면 처음부터 다시 함)
1. **생성 직전 4종 확인 + 프리뷰 승인** — 모델·해상도·오디오·비율을 표로 보여주고 사용자 OK를 받은 뒤에만 호출. (CLAUDE.md 규칙 5)
2. **덮어쓰기 금지** — 수정할 때마다 새 버전 폴더(`v{날짜}_v2`, `_v3`…)와 새 HTML로 누적. HTML도 그 버전 폴더 **안에** 저장. (메모리: feedback-version-never-overwrite)
3. **생성 이미지를 Read 도구로 열지 않는다** — 경로만 안내하고 사용자가 직접 확인. (컨텍스트 절약 + 20MB 제한)
4. **상표·실존 브랜드명 금지** — "애플워치"가 아니라 "티타늄 케이스에 오렌지 액션 버튼" 식으로 **디자인 언어**로 묘사. (필터 회피 + 법적 안전)
5. **강화 프롬프트 기본 주입(v2 표준)** — 모든 이미지 생성에 `IMG_ENHANCE`, 모든 영상 생성에 `VID_ENHANCE`를 항상 합쳐서 호출한다. (아래 [★ 필수 강화 프롬프트] 섹션. 시네마틱 실사·로우키·정면/아이레벨 배제·로우/하이/더치·데마이·매치컷 개연성 / 영상 다이내믹 무브먼트 강제.)
6. **★v3 표준(Splitline 세션 반영) — 시작 전 [부록 E]를 먼저 읽는다.** 모델 선택(인물=nano_banana_2, gpt-image 금지)·단독 얼굴 CU 문법·시트 재조명·한글 타이포 QA·루마키/크로마 파이프라인·병렬 운영의 확정 정답이 정리돼 있다. 시행착오 #21~#36. (→ `04_reference_lessons-appendix.md` 부록 E)

---

## ★ 필수 강화 프롬프트 (이미지·영상 기본 주입) — v2 표준

> 이번 AETHER 세션에서 확정된 품질 기준. **모든 컷 생성 시 아래 두 상수를 프롬프트에 기본 주입**한다(프로젝트 무관 재사용). 이미지 생성 호출의 공통 프롬프트(COMMON)에 `IMG_ENHANCE`를, 영상 프롬프트 빌더에 `VID_ENHANCE`를 항상 합친다. 이미지/영상 프롬프트는 모델 입력용이라 영어로 적는다(humanizer 미적용).

### 1) IMG_ENHANCE — 이미지 강화 (모든 이미지 컷 공통)
의도(한글): 더 시네마틱한 실사 + **얼굴 디테일 강화** / **정면·아이레벨 화각 전면 삭제**(렌즈 응시 금지) / 로우·하이·**더치 앵글** + 다이내믹 광각 + **데마이(얕은 심도) 클로즈업** 적극 / **하이키 금지, 로우키 고급** / 컷 간 **매치컷·트랜지션 개연성** / 영상화 시 다이내믹하게 살아나는 키프레임.

```text
CINEMATIC PHOTOREAL — REQUIRED ENHANCEMENT (append to every image prompt):
Heightened photoreal realism with ENHANCED FACIAL DETAIL (lifelike skin micro-texture, visible pores, subsurface scattering, sharp eye catchlights); a real frame from a premium TV commercial, never CGI / 3D-render / illustration.
ABSOLUTELY NO front-facing and NO eye-level framing — the subject never looks straight into the lens; no honest flat eye-level full shots.
Aggressively use TV-CF camera grammar (화각·구도): LOW-ANGLE, HIGH-ANGLE and DUTCH-ANGLE compositions; off-center rule-of-thirds; dynamic WIDE-ANGLE perspectives AND shallow-depth-of-field telephoto CLOSE-UPS (demai bokeh) with clear 3-layer FG/MG/BG depth.
BACKLIGHT MANDATORY (역광/림라이트): hard warm back-light / rim-light from behind tracing the subject's silhouette and separating it from the background; motivated key from window/blinds; NO flat frontal fill.
NEGATIVE FILL MANDATORY (네거티브 필): black negative fill on the shadow side — one side falls into deep controlled shadow to sculpt the form and raise contrast; kill flat ambient.
LOW-KEY luxurious grade (NEVER high-key): deep controlled shadows, restrained highlights, premium cinematic mood matching the reference.
Compose so each cut CONNECTS to its neighbours via match-cuts / natural transitions — strengthen narrative continuity and context across cuts.
Frame it as a keyframe primed for dynamic video motion (built-in movement potential).
```

### 2) VID_ENHANCE — 영상 강화 (모든 영상 컷 공통)
의도(한글): **① 오디오는 무조건 BGM 없이 효과음(SFX)만**(가장 강한 고정 규칙 — 규칙 0 [B] 참조, BGM·내레이션은 후반 합성) / ② 컷 상황에 맞게 핸드헬드·dolly in·arc·로봇암 등 **다이내믹 무브먼트를 반드시** 넣고 컷 간 매치컷/트랜지션으로 연결. (단, 크로마키 플레이트 영상은 키잉을 위해 **locked-off 고정 카메라** 예외 — 부록 E 참조.)

```text
DYNAMIC MOTION — REQUIRED ENHANCEMENT (the audio line MUST be first on every video prompt):
No background music. NO BGM. NO score. SFX only — at most a few subtle diegetic sound effects; no musical bed whatsoever.
Every clip MUST carry deliberate dynamic camera movement chosen to fit the cut — handheld energy, dolly / push-in, arc / orbit, crane-up / pull-up, ROBOT-ARM dynamic sweep, crash-zoom, tilt-up, over-the-shoulder telephoto. (EXCEPTION: chroma-green plate clips stay LOCKED-OFF static for clean keying — only the subject moves.)
Write a real moving-shot keyframe (mid-action + motion blur), and add a match-cut / transition link to the adjacent cut.
```

> **적용 위치:** GATE 6 체크리스트에 LOW-KEY·NO-eye-level·더치/로우/하이·데마이·**역광 림라이트·네거티브 필**을 기본 ON / GATE 8 프리뷰에 **"규칙 0 MANDATORY 프리픽스 + 강화 상수 주입됨"** 표기 / GATE 9 이미지 `COMMON += 규칙0[A] + IMG_ENHANCE` / GATE 12 영상 프롬프트 = **`규칙0[B](No BGM·SFX only)` 를 맨 앞에 두고** `+= VID_ENHANCE`. 컷별 추천 영상 프롬프트(GATE 17 자동입력용 `video_prompts.json`)에도 **맨 앞 줄에 No-BGM/SFX-only**를 박고 컷 상황에 맞는 카메라 무브를 미리 넣어둔다.
> **유형별 확장 상수**(`IMG_ENHANCE_PERSON`/`IMG_ENHANCE_OBJECT`, `VID_ENHANCE_SFX`/`VID_ENHANCE_OBJECT`)의 풀텍스트는 `03_reference_enhance-prompts.md` 참조.

---

## 전체 흐름

```
[시작 전]
G0 생성 엔진 연결 확인 (Higgsfield CLI/MCP · Magnific — 최소 하나, 안 되어 있으면 연결 먼저) → 

[기획·스토리보드]
G1 제품 정의 → G2 광고 접근방식 ★ → G3 감정 서사 컨셉 ★ → G4 주인공·관계·공간
→ G5 3막 구조 & 제품의 역할 → G6 비주얼 문법 → G7 일관성 전략
→ [기획안 정리·승인] → G8 생성 전 체크
→ G9a gpt_image_2 · 16:9 · 1K High — 30컷 프리뷰 시트 1장 생성 → [구성 확인]
→ G9a-rev nano_banana Pro · 16:9 · 2K · 1/4 · Unlimited ON — 수정 컷 개별 생성 (반복)
→ G9a-final gpt_image_2 · 16:9 · 2K · High quality — 최종 확인 시트 재생성 → [승인]
→ G9b nano_banana Pro · 16:9 · 2K · 1/4 · Unlimited ON — 30개 개별 이미지 일괄 생성(+에러)
→ G10 HTML 빌드·검수 → G11 수정=새 버전

[제작 — 스토리보드 확정 후]
→ G12 영상화(Seedance) → G13 BGM(Suno 프롬프트→사용자 생성) → G14 내레이션 VO(ElevenLabs MCP 기본, 백업 Higgsfield TTS)
→ G15 로고(투명 PNG) → G16 최종 완성 스토리보드 조립(기획안+VO 포함)

[리뷰·수정 — 생성물마다]
→ G17 인터랙티브 리뷰·수정 콘솔 (자동 팝업 HTML에서 컷 선택→수정요청 Enter→즉시 재생성)
```

★ = 가장 많이 갈아엎은, 제일 중요한 분기. (G1~G11은 한 번에, G12~G17은 스토리보드 확정 뒤 순서대로/선택적으로.)

> **BGM은 API로 자동생성하지 않는다.** GATE 13에서 Suno 프롬프트를 제안하고, 사용자가 직접 Suno에서 생성해 후반 편집(최종 조립 / 부록 C-4 프리미어)에서 얹는다.

---

## 막혔을 때의 황금 규칙

사용자가 제안을 계속 "별로"라고 하면 같은 걸 또 던지지 말고 — ① **피하고 싶은 점 한 줄**을 물어 키워드를 받거나, ② **실존 레퍼런스 광고를 웹에서 분석**해 그 문법으로 다시 제안한다(GATE 2 참고). 무한 재생성은 토큰·시간 낭비.
