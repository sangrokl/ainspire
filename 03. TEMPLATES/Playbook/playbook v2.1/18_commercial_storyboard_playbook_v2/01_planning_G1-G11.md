# 🎯 01_planning_G1-G11.md — 기획·스토리보드 (GATE 1~11)

---

## 🚪 GATE 1 — 제품·브랜드 정의

**왜:** 무엇을, 누구에게, 어떤 톤으로 파는지 모르면 어떤 장면도 못 만든다.

### ❓ Q1-1. 무엇을 광고하나? (자유 입력 받되 카테고리 확인)
- 예: 에너지드링크 / 스마트워치 / 화장품 / 앱 …

### ❓ Q1-2. 브랜드 톤은? (객관식)
| 선택 | 의미 | 결과 비주얼 |
|---|---|---|
| A. 프리미엄·고급 | 비싸 보이고 절제된 | 로우키 조명, 깊은 그림자, 미니멀 |
| B. 친근·따뜻 | 일상적이고 다정한 | 밝은 텅스텐, 생활감 |
| C. 강렬·역동 | 에너지·스피드 | 고대비, 강한 색, 다이내믹 앵글 |
| D. 미니멀·시크 | 세련·도시적 | 모노톤, 여백, 정제 |

### ❓ Q1-3. 상표를 어떻게 가릴까? (객관식 — 거의 항상 필요)
- A. **디자인 언어로 묘사** [추천] — 로고/이름 대신 형태·색·소재로. (예: "세로 워드마크가 있는 매트 네이비 캔 + 번개 마크")
- B. 가상의 브랜드명 새로 만들기
- C. 노출 없음(제품 형태만)

> **시행착오 #1:** 실존 브랜드명을 그대로 넣으면 생성 필터에 걸리거나 법적으로 위험하다. 처음부터 "design language(디자인 언어)"로 적어두면 끝까지 안전하다.

**산출물:** 제품명/카테고리, 톤(A~D), 상표 표현 방식.

---

## 🤖 AUTO-G1.5 — TVCF 레퍼런스 에이전트 (G1 확인 즉시 자동 실행)

**트리거:** G1 산출물(제품 카테고리)이 확정되는 즉시 — 사용자가 별도 요청 없이도 — 에이전트가 아래를 자동 수행한다.

### 에이전트 수행 순서
1. **WebSearch 3회** (병렬)
   - `"<카테고리> TVCF award winning commercial archetype"`
   - `"best <카테고리> commercials Cannes Lions breakdown"`
   - `"<카테고리> ad storytelling structure analysis"`
2. **아키타입 추출** — 수상작·화제작에서 반복되는 문법 패턴 **최소 7개** 추출
3. **표 생성** — 아래 형식으로 정리:

| # | 아키타입 (EN label) | 훅 (0–5초) | 구조 (Beat 흐름) | 톤 | 어울리는 제품 | 대표 TVCF 예시 |
|---|---|---|---|---|---|---|
| 1 | 이름 | 첫 5초 장치 | 3막·비트 순서 | 색감·감정 | 제품 유형 | 브랜드·연도 |

4. **추천 정렬** — G1에서 확정된 **우리 제품·톤** 기준으로 가장 잘 맞는 순서로 번호 재정렬, 이유 한 줄씩 추가

### 산출물
- 대화에 인라인 표로 즉시 출력
- `projects/{project}/{version}/tvcf_archetypes.md` 에 저장 (G2 입력값으로 재사용)

> **이 표가 없으면 GATE 2 Q2-2로 진행하지 않는다.** 표 생성 완료 후 사용자에게 선택을 물어본다.

---

## 🚪 GATE 2 — 광고 접근 방식 ★ (가장 중요)

**왜:** 여기서 전체 광고의 격이 갈린다. 이번 프로젝트에서 **네 번**을 여기서 갈아엎었다.

### ❓ Q2-1. 어떤 방식으로 보여줄까? (객관식)
| 선택 | 방식 | 느낌 |
|---|---|---|
| A. 제품 기능 나열형 | 매 컷 제품을 보여주고 기능을 차례로 소개 | ⚠️ 쉽지만 **촌스럽고 1차원적** |
| B. **애플식 일상 감정 내러티브** [추천] | 한 사람의 감정 이야기 안에 제품이 자연스럽게 녹음 | 고급스럽고 공감됨 |
| C. 무드/비주얼 필름 | 대사·서사 없이 분위기와 미감으로 | 감각적, 브랜딩용 |

> **시행착오 #2 (이번 프로젝트의 핵심 교훈):**
> HALO를 처음엔 "공간마다 시계 기능 보여주기"(A형)로 만들었더니 사용자가 *"계속 시계만 노골적으로 나오는 방식은 촌스럽다", "너무 1차원적이야, 애플 광고처럼"* 이라고 했다.
> → **제품을 매 컷 들이대지 마라.** 제품은 삶에 녹아 있다가 **결정적 순간에만** 의미를 갖고, 제품 히어로샷(클로즈업)은 **맨 마지막 피날레로 미룬다.**
> → 거의 항상 **B를 추천**한다. A를 고르면 위 경고를 반드시 사용자에게 한 번 더 알린다.

### ❓ Q2-2. (감정 서사도 다 별로일 때) 레퍼런스 광고 문법으로 (객관식)
제안한 서사가 계속 안 통하면, **AUTO-G1.5에서 이미 생성된 `tvcf_archetypes.md` 표를 꺼내 선택지로 제시한다.** 표가 없으면 지금 바로 AUTO-G1.5 에이전트를 실행하고 완료 후 이 질문으로 돌아온다.

> **시행착오(HALO 최종):** 감정 서사를 다 "별로"라고 한 뒤, 카테고리 TVCF를 **실제로 웹 검색·분석**해서 아키타입을 제안 → 사용자가 선택. **막히면 레퍼런스를 분석하라 — AUTO-G1.5가 이걸 자동화한다.**

**산출물:** 접근 방식(A/B/C) 또는 차용할 레퍼런스 문법.

---

## 🚪 GATE 3 — 감정 서사 컨셉 ★ (B형일 때)

**왜:** "어떤 감정 이야기냐"가 30컷 전체 방향을 가른다. 비싼 생성 전에 **반드시** 먼저 정한다.

### ❓ Q3-1. 주인공의 감정 through-line(관통선)은? (객관식)
한 명의 주인공 + 하루~며칠의 자연스러운 일상. 제품은 결정적 순간에만 의미.

| 선택 | 서사 | 한 줄 줄거리 | 제품의 역할 |
|---|---|---|---|
| A. 회복·성장 | 바빠서 자신을 놓았던 사람이 다시 시작 | 작은 분투 → 작은 성취 → 의미 있는 결승선 | 조용히 곁에서 응원·기록 |
| B. 관계·연결 | 떨어져 있는 소중한 사람과의 거리 | 그리움 → 하루 종일 작은 연결 → 재회 | 두 사람을 잇는 보이지 않는 끈 |
| C. 자기돌봄·번아웃 | 치열한 하루를 버텨내는 사람 | 압도 → 조용한 챙김 → 작은 평온 | 나를 지켜봐 주는 존재 |
| D. 성취·도전 | 목표를 향한 개인의 여정 | 결심 → 한계 → 돌파 | 여정의 동반자·증거 |

### ❓ Q3-2. 시간 배경은? (객관식)
- A. 하루(아침→밤) / B. 며칠(다른 날들 OK) / C. 특정 순간 하나를 길게

**산출물:** 감정 컨셉(A~D), 한 줄 로그라인, 시간 배경.

---

## 🚪 GATE 4 — 주인공·관계·공간

**왜:** 공간과 인물이 많으면 산만해지고 개연성이 무너진다.

### ❓ Q4-1. 공간(장소)은 몇 개? (객관식)
| 선택 | 개수 | 비고 |
|---|---|---|
| A. 1곳 집중 | 한 공간 | 가장 응집력 높음 |
| B. **2곳 교차** [추천] | 두 공간을 오감 | 변화 + 개연성 균형 |
| C. 3곳 이상 | ⚠️ 산만해지기 쉬움 |

> **시행착오 #3:** HALO를 5개 공간으로 펼쳤더니 *"너무 장소와 상황이 많다"* 는 피드백. → **1~2곳으로 줄이고** 교차/반복으로 공감의 밀도를 높여라.

### ❓ Q4-2. 2번째 인물(연인·아이·동료 등)이 등장하나? (객관식)
- A. 주인공 1명만
- B. 등장하지만 **얼굴은 안 보이게** [추천 — 일관성 안전] (실루엣·뒷모습·손·사진·화면으로)
- C. 얼굴까지 또렷이 등장 (→ 별도 얼굴 레퍼런스 필요, 난이도↑)

> **시행착오 #4:** AI는 같은 얼굴을 두 사람분 일관되게 그리기 어렵다. 2번째 인물은 실루엣/손/뒷모습/폰화면으로 처리하면 얼굴 일관성 문제를 통째로 피한다.

### ❓ Q4-3. 의상 전략 (객관식)
- A. 공간/상황마다 의상 교체 (얼굴만 고정)
- B. 일관된 한 룩

**산출물:** 공간 수, 2번째 인물 처리법, 의상 전략.

---

## 🚪 GATE 5 — 3막 구조 & 제품의 역할

**왜:** 30컷을 막연히 나열하면 이야기가 안 된다. 3막으로 뼈대를 잡는다.

### 기본 30컷 배분 (B형 내러티브 기준, 조정 가능)
| 막 | 컷 수 | 내용 | 제품 노출 |
|---|---|---|---|
| 1막 (도입) | ~8컷 | 주인공·상황·결핍/그리움 설정 | 거의 없음, 1~2회 감정적 등장 |
| 2막 (전개) | ~10컷 | 일상 속 작은 사건·연결, 감정 쌓기 | 결정적 순간에만 2~3회 |
| 3막 (해소) | ~6컷 | 목표 달성/재회 = 감정의 payoff | 감정과 함께 |
| 피날레 | ~6컷 | **제품 히어로샷/매크로/브랜드** | ★ 여기 몰아서 |

### ❓ Q5-1. 제품의 "결정적 순간"을 몇 개로? (객관식)
- A. 3개 이하 [추천 — 절제] / B. 4~5개 / C. 그 이상(⚠️ 기능 데모로 회귀 위험)

> **시행착오 #5:** 남기는 제품 컷도 **기능 데모가 아니라 감정 순간**으로 적어라.
> 나쁜 예) "심박수 120 표시되는 화면" → 좋은 예) "집에서 보내온 하트비트가 손목에 도착하며 번지는 온기".

**산출물:** 막별 컷 배분, 제품 결정적 순간 목록(감정 문장으로).

---

## 🚪 GATE 6 — 비주얼 문법 (촬영·미술)

**왜:** 같은 이야기도 렌즈·조명·미술이 격을 만든다.

### ❓ Q6-1. 컬러 그레이드(색 분위기) 흐름 (객관식)
- A. 단색 유지 / B. **감정 따라 변화** [추천] (예: 차가운 블루 → 연결 순간 따뜻한 텅스텐 스밈 → 골든 온기)
- 막마다 다른 grade 이름을 정해두면 일관성이 산다. (예: AWAY/WARM/HOME/FIN)

### ❓ Q6-2. 카메라·렌즈 기본값 (보통 전부 ON)
- ☑ **데마이(망원 얕은 심도)** — 배경이 보케로 녹는 클로즈업.
- ☑ **역광·림라이트 실루엣** — 인물을 배경에서 분리, 입체감.
- ☑ **매치컷** — 앞 컷의 형태/동작을 다음 컷이 이어받아 부드럽게 전환.
- ☑ 거울/유리 반사 인서트 — 두 공간/세계를 한 프레임에.
- ☒ **정면·아이레벨·풀샷 금지** — 카메라를 똑바로 응시하거나 전신을 멀리서 잡으면 광고가 싸 보인다.

### ❓ Q6-3. 배경 미술 (★ 항상 ON)
- ☑ **화면을 꽉 채운다** — 빈 공간(데드 스페이스) 없이 전경-중경-후경 레이어.
- ☑ 소품마다 의도적 배치 + **컬러 콘트라스트**.
- 단, 로고가 들어갈 자리는 의도적 여백(negative space)으로 비운다.

> **시행착오 #6:** 초기 버전이 "촌스럽다"고 한 큰 이유 중 하나가 **빈 배경**이었다. `ARTDIR` 상수로 모든 컷에 공통 적용하라.

**산출물:** grade 흐름, 카메라/미술 체크리스트.

---

## 💉 ★ 필수 강화 프롬프트 — 요약 + 포인터

> 모든 이미지에 `IMG_ENHANCE`, 모든 영상에 `VID_ENHANCE`를 기본 주입한다.  
> **풀텍스트 및 유형별 확장 상수(`IMG_ENHANCE_PERSON`, `IMG_ENHANCE_OBJECT`, `VID_ENHANCE_SFX`, `VID_ENHANCE_OBJECT`) 전체는 `03_reference_enhance-prompts.md` 참조.**  
> 이미지/영상 프롬프트는 모델 입력용이라 영어로 적는다.

---

## 🚪 GATE 7 — 일관성 전략 (얼굴·제품 고정)

**왜:** 컷마다 주인공 얼굴/제품 모양이 바뀌면 광고가 안 된다.

### 🔑 핵심 기법: img2img (참조 이미지로 생성)
- **레퍼런스 이미지(REF)** 를 Higgsfield MCP에 업로드해 생성하면 그 얼굴/제품을 유지한다.
  - `media_upload(files[])` → presigned URL에 PUT → `media_confirm` → `generate_image({model, prompt, resolution, medias:[{role:'image', value:media_id}]})`
- 보통 2장: **주인공 얼굴 1장 + 제품 목업 1장**.
- 컷 성격에 따라 ref 조합을 다르게: 인물 컷=얼굴ref, 제품클로즈업=제품ref, 둘 다 나오면 둘 다.
- 의상은 바꾸되 얼굴만 고정하려면 프롬프트에 *"preserve ONLY the exact facial identity, change wardrobe to ___"* 식으로 명시.

### ❓ Q7-1. 레퍼런스 이미지 준비됐나? (객관식)
- A. 있다(경로 확인) / B. 먼저 만들어야 함(주인공·제품 키비주얼 1차 생성부터)

> **시행착오 #7:** 2번째 인물은 ref로 얼굴을 잠그려 하지 말고 GATE 4-2처럼 실루엣/손/화면으로 처리. 주인공만 얼굴 ref를 건다.

**산출물:** 주인공 ref 경로, 제품 ref 경로.

---

## 📋 ▣ 중간 정리 — 기획안(BRIEF) 작성·승인

여기까지의 답을 모아 **기획안**을 표로 정리해 사용자에게 보여주고 승인받는다. 형식 예:

```
[제품] 톤 / 상표표현
[접근] B 애플식 내러티브
[서사] 컨셉 + 로그라인 + 시간배경
[인물/공간] 주인공 / 2번째인물 처리 / 공간 N개 / 의상
[구조] 1막~피날레 컷 배분 + 제품 결정적순간 목록
[비주얼] grade 흐름 / 카메라·미술 체크리스트
[일관성] ref 경로
[저장] projects/{name}/v{날짜}/...
```
승인 후에야 컷별 프롬프트 작성 → 생성으로 간다.

---

## 🚪 GATE 7.5 — 30컷 스토리 작성·승인 ★

**왜:** 기획안은 방향이고 스토리는 실행이다. 비싼 이미지 생성 전에 30컷 전체를 텍스트로 완성·승인받아야 방향이 어긋난 생성 낭비를 막는다.

> **이 게이트는 BRIEF 승인 직후, G8(생성 전 체크) 직전에 반드시 실행한다.**

### ❓ G7.5 진행 방식 (에이전트 행동 규칙)

1. **에이전트가 30컷 전체를 직접 작성한다** — 사용자에게 묻지 않고, BRIEF에서 확정된 요소(로그라인·3막 구조·컬러 그레이드·카메라 규칙·제품 결정적 순간)를 그대로 반영해 30컷 시나리오 테이블을 생성한다.
2. **표 형식으로 먼저 보여준다** — 컷 번호 / 막 / 길이 / 샷 타입 / 장면 한 줄 / 제품 역할 / 사운드 6열 테이블. 사용자가 전체 흐름을 한눈에 검토할 수 있게.
3. **총 길이 합계를 표 아래에 명시한다** — 30초 목표와 맞는지 확인. 맞지 않으면 조정 후 재제시.
4. **제품 결정적 순간(★)을 별도로 요약한다** — 컷 번호 + 감정 문장.
5. **사용자 승인을 받는다** — 수정 요청 시 해당 컷만 수정 후 재제시. 전면 수정 시 로그라인·3막 구조부터 다시.
6. **승인 후 `scenario.md`로 저장한다** — 아래 포맷으로 `projects/{project}/{version}/scenario.md`에 30컷 전체 저장.

---

## 📝 ★ 시나리오 산출물 포맷 — 컷별 마크다운 구조

BRIEF 승인 후 컷별 프롬프트는 아래 마크다운 구조로 한 컷씩 작성해 `projects/{project}/{version}/scenario.md`에 30개 컷 전체를 누적한다. GATE 8 프롬프트 프리뷰 테이블·G9a 이미지 프롬프트(`[first frame]`)·GATE 12 영상 프롬프트(`[video prompt]`)·사운드 디자인(`[sound]`)이 모두 이 파일 하나에서 파생된다 — 컷마다 흩어져 있던 정보를 한 곳에 모아둔다.

### 포맷
```
## Cut 01
[duration]: 1.0s
[shot]: ECU eye reflection
[first frame]: Extreme close-up on JUNE's eye, a tiny strawberry reflected in the iris, soft window light, shallow depth of field
[video prompt]: RUNTIME: 4 seconds. / CAMERA: ARRI ALEXA Mini LF, ZEISS, anamorphic 2.39:1. / TIME: soft morning light. / CHARACTER: JUNE, same face as reference. / SHOT GROUP — 4 SECOND SEQUENCE: BEGINS WITH (0:00-0:01) eye in stillness / ACTION (0:01-0:02) blinks slowly, reflection shimmers / TRANSITION (0:02-0:03) pupil contracts / ENDS WITH (0:03-0:04) macro hold on strawberry reflection. / LIGHT: soft window backlight, gentle negative fill. / SFX: soft inhale, distant chime.
[sound]: soft inhale, distant chime
```

### 필드 설명
| 필드 | 내용 | 비고 |
|---|---|---|
| `[duration]` | **최종 편집상의 컷 길이**(초) — 컷마다 다르게 줄 수 있다(0.5~5s 등, 더 이상 전부 고정 아님) | **전체 합이 목표 광고 길이(보통 30s)와 맞는지 GATE 8에서 합계 검증.** ⚠️ 이는 GATE 16 최종 조립 시 트림 기준이며, Kling 3.0 Turbo(기본) 실제 생성 길이와는 다르다 — **생성은 항상 4초 고정**(변경하지 않음), `[duration]`이 4초보다 짧으면 4초로 그대로 생성한 뒤 최종 조립에서 잘라낸다. |
| `[shot]` | 샷 타입·앵글 한 줄 요약 (예: ECU eye reflection, OTS wide, dutch-angle macro) | GATE 6 비주얼 문법과 일치해야 함 |
| `[first frame]` | 정지 첫 프레임(이미지) 생성 프롬프트의 장면 묘사 | G9a/G9b 호출 시 규칙0[A]+IMG_ENHANCE(또는 PERSON/OBJECT)가 자동으로 합쳐진다 — 여기엔 장면만 적는다 |
| `[video prompt]` | 영상 생성 프롬프트(기본 Kling 3.0 Turbo, 백업 Seedance 2.0) — `03_reference_enhance-prompts.md`의 `VIDEO_PROMPT_FORMAT` 필드 순서(RUNTIME→CAMERA→TIME→CHARACTER→SHOT GROUP[BEGINS WITH/ACTION/TRANSITION/ENDS WITH 타임스탬프 비트]→LIGHT→SFX)를 그대로 따른다 | GATE 12 호출 시 규칙0[B](No BGM·SFX only)가 맨 앞에 자동으로 합쳐진다. **전체 700자 이내**(공백 포함) — 넘으면 SHOT GROUP 비트 묘사부터 줄인다. SHOT GROUP 4비트 합은 항상 4초 |
| `[sound]` | 효과음 디자인 | diegetic SFX만 — **BGM·내레이션 절대 금지**(규칙0[B], BGM은 GATE 13 별도) |

### 저장 위치·버전 규칙
- `projects/{project}/{version}/scenario.md` — `## Cut 01`~`## Cut 30` 전체를 한 파일에 누적.
- 수정 시 새 버전 파일로 누적(`scenario_v2.md` 등) — GATE 11 "수정 = 새 버전, 덮어쓰기 금지" 원칙과 동일.

---

## 🚪 GATE 8 — 생성 전 체크 (필수 4종 + 프리뷰)

> **이 표는 개별 컷 생성(G9a-rev·G9b) 기본값이다.** G9a·G9a-final 프리뷰 시트는 별도 모델·해상도(`gpt_image_2`, 1K High → 2K High)를 쓴다 — 각 단계 표는 GATE 9의 해당 절을 따른다. 4단계 모두 호출 직전 그 단계의 표를 보여주고 승인받는다(절대 규칙 1).

생성 호출 **직전** 반드시 표로 보여주고 OK 받는다 (개별 컷 생성 기준):

| 항목 | 기본값 |
|---|---|
| MODEL | Higgsfield `nano_banana_2` 또는 Magnific `imagen-nano-banana-2`(NB Pro)/`seedream-4` |
| 해상도 | 2k (2752×1536) |
| 비율 | 16:9 |
| 오디오 | N/A (정지 이미지) |
| 컷 수 | 30 |
| ref medias role | `image` (호출 전 `models_explore(action='get', model_id='nano_banana_2')`로 resolution 라벨·medias role 확정) |

> **모델 파라미터 확정:** 생성 전 반드시 모델 파라미터를 확인한다 — CLI `higgsfield model get nano_banana_2 --json` / Higgsfield MCP `models_explore(action='get', model_id='nano_banana_2')` / Magnific `images_models_show`. Higgsfield 대안 `gpt_image_2`. 엔진별 플로우는 `00_core.md`의 [생성 엔진] 참조.

그리고 `scenario.md`(★ 시나리오 산출물 포맷)에서 파생한 **컷별 프롬프트 프리뷰 테이블(한글 요약)** 을 함께 보여준다. (#·막·장면·제품역할)  
프리뷰에 **"규칙 0 MANDATORY 프리픽스 + IMG_ENHANCE 주입됨"** 표기. 이때 `scenario.md`의 `[duration]` 합계가 목표 광고 길이(보통 30s)와 맞는지 검증한다.

---

## 🚪 GATE 9 — 생성 실행 & 에러 핸들링 (Higgsfield CLI/MCP · Magnific 플로우)

> **4단계 생성 원칙:** 컷마다 바로 최종본을 뽑지 않는다.
> ① G9a — gpt_image_2 · 16:9 · 1K High로 30컷 프리뷰 시트 1장 생성 → 전체 구성 확인
> ② G9a-rev — 수정 필요 컷만 nano_banana Pro · 16:9 · 2K · 1/4 output · Unlimited ON으로 개별 생성
> ③ G9a-final — 수정 완료 후 16:9 · 2K · High quality로 최종 확인 시트 재생성 → 승인
> ④ G9b — 만족하면 nano_banana Pro · 16:9 · 2K · 1/4 output · Unlimited ON으로 30개 개별 이미지 일괄 생성

---

### 1️⃣ G9a — 프리뷰 시트 (gpt_image_2 · 16:9 · 1K High · 단일 호출)

**목적:** 30컷 전체 구성·구도·색감을 1장의 Hollywood pre-vis 스토리보드 시트로 빠르게 확인.

**출력 사양:**
| 항목 | 값 |
|---|---|
| 모델 | `gpt_image_2` |
| 비율 | 16:9 (와이드) |
| 해상도 | 1K · `quality: "high"` 강제(기본값 low — 반드시 명시) |
| 레이아웃 | 5행 × 6열 = 30프레임, 얇은 다크 보더 구분 |
| 프레임 번호 | 각 프레임 좌상단 — 소형 검정 탭 + 흰 숫자 01~30 |

```
# MCP 경로
generate_image({
  model: "gpt_image_2",
  prompt: "Hollywood cinematic pre-visualisation storyboard sheet. Single page, 16:9 wide format. 5 rows × 6 columns = 30 sequential frames, each frame separated by a thin dark border. Each frame has a small solid-black tab at its top-left corner with a white two-digit frame number (01–30). High quality. The frames depict: [컷 01 장면 한 줄] … [컷 30 장면 한 줄]. " + 규칙0[A] + IMG_ENHANCE,
  resolution: "1k",
  aspect_ratio: "16:9",
  quality: "high"
}) → preview/storyboard_sheet_v1.png

# CLI 경로
higgsfield generate create gpt_image_2 \
  --prompt "Hollywood cinematic pre-vis storyboard sheet. 16:9, 5×6 grid, 30 frames, black tab + white number 01–30 top-left each frame. [컷별 장면 요약] " \
  --aspect_ratio 16:9 --resolution 1k --quality high --wait
```

- 저장: `projects/{project}/{version}/preview/storyboard_sheet_v1.png`
- 생성 후 경로만 전달 — Read 도구로 열지 않음(규칙 3).
- 수정 필요 컷이 있으면 → **G9a-rev**. 구성 전체 OK면 → **G9a-final**.

---

### 2️⃣ G9a-rev — 개별 컷 수정 (nano_banana Pro · 16:9 · 2K · 1/4 output · Unlimited ON)

**목적:** G9a 시트에서 구성이 마음에 들지 않는 컷만 개별로 뽑아 확인·수정한다.

**생성 사양:**
| 항목 | 값 |
|---|---|
| 모델 | `nano_banana_2` (Pro) |
| 비율 | 16:9 |
| 해상도 | 2K |
| output | 1/4 |
| Unlimited | ON |

```
# MCP 경로 (수정 컷 1개)
generate_image({
  model: "nano_banana_2",
  prompt: [해당 컷 장면묘사] + 규칙0[A] + IMG_ENHANCE + GRADE,
  resolution: "2k",
  aspect_ratio: "16:9",
  output_count: 1,        # 1/4 output
  unlimited: true         # Unlimited toggle ON
}) → preview/rev/cut_NN_v1.png

# CLI 경로
higgsfield generate create nano_banana_2 \
  --prompt "<규칙0[A]+IMG_ENHANCE+GRADE+장면>" \
  --aspect_ratio 16:9 --resolution 2k --wait
```

- 저장: `projects/{project}/{version}/preview/rev/cut_NN_vN.png`
- 수정 컷이 만족스러우면 해당 컷 확정. 모든 컷 수정 완료 후 → **G9a-final**.
- 만족스럽지 않으면 프롬프트 수정 후 동일 사양으로 재생성(덮어쓰기 금지 — 새 버전 번호).

---

### 3️⃣ G9a-final — 최종 확인 시트 (16:9 · 2K · High quality · 승인용)

**목적:** 개별 수정이 모두 끝난 뒤, 확정된 프롬프트로 고품질 시트를 재생성해 최종 승인을 받는다.

**생성 사양:**
| 항목 | 값 |
|---|---|
| 모델 | `gpt_image_2` |
| 비율 | 16:9 |
| 해상도 | 2K · `quality: "high"` 강제(기본값 low — 반드시 명시) |
| 레이아웃 | 5행 × 6열, 번호 01~30 (G9a 동일 포맷) |

```
generate_image({
  model: "gpt_image_2",
  prompt: "Hollywood cinematic pre-visualisation storyboard sheet. Single page, 16:9 wide. 5 rows × 6 columns = 30 frames, thin dark border, black tab + white number 01–30 top-left. High quality. [확정된 컷별 장면 묘사] " + 규칙0[A] + IMG_ENHANCE,
  resolution: "2k",
  aspect_ratio: "16:9",
  quality: "high"
}) → preview/storyboard_sheet_final.png
```

- 저장: `projects/{project}/{version}/preview/storyboard_sheet_final.png`
- 사용자가 최종 시트를 보고 **만족하면 → G9b**. 추가 수정이 있으면 → G9a-rev로 돌아가 해당 컷만 재수정 후 G9a-final 재생성.

---

### 4️⃣ G9b — 30개 개별 이미지 일괄 생성 (nano_banana Pro · 16:9 · 2K · 1/4 output · Unlimited ON)

**목적:** G9a-final 승인 후, 확정된 프롬프트 그대로 ref 적용해 30개 개별 이미지를 생성한다.

> **개별 컷(및 재생성) 생성 시 반드시 참조할 2종:**
> 1. **승인된 `storyboard_sheet_final.png`(G9a-final)** — **구도·배열·막 흐름만** 기준으로 삼는다. **이 시트의 조명은 참조하지 않는다** — 시트는 빠른 프리뷰용 합성이라 조명이 균일/평탄할 수 있고, 그걸 그대로 따라가면 시네마틱이 죽는다(시행착오 #25와 동일 원리). 프롬프트에 "구도(카메라 앵글·배치·뎁스 레이어)는 시트를 따르되, 조명은 무시하고 규칙0[A]+IMG_ENHANCE의 로우키·웜 백라이트 림·네거티브 필로 재조명(relight)한다"를 명시 — LOOK OVERRIDE.
> 2. **최신 레퍼런스 이미지** — 1차 얼굴 레퍼런스(`projects/{project}/{version}/ref/ref_face.png`)는 사진 5장 이상 있으면 Soul Character 학습으로 만든다(`03_reference`의 `SOUL_CHARACTER_TRAINING`, 부록 E #39 — 동일 인물은 `soul_id` 재학습 없이 재사용). 5장 미만이면 `gpt_image_2` 턴어라운드 시트(`CHAR_TURNAROUND_SHEET`, 부록 E #37)로 대체. 만족스러운 컷이 나오면 그 컷으로 레퍼런스를 다시 뽑아(`ref_face_v2.png` 등) 갈아끼운다. **개별 컷 이미지 생성은 `nano_banana_2`로 통일한다 — `soul_2`는 1차 레퍼런스 스틸 생성에만 쓰고 개별 컷에는 미사용**(부록 E #38). `nano_banana_2`는 얼굴·제품 레퍼런스를 동시에 여러 장 첨부할 수 있으므로, **모든 생성 호출에 해당하는 레퍼런스 이미지(얼굴·제품)를 항상 medias로 첨부**한다. 새 레퍼런스가 나오면 이후 모든 개별 컷·재생성은 그걸 기준으로 한다(레퍼런스도 새 버전 파일로 누적, 덮어쓰기 금지).

**생성 사양:**
| 항목 | 값 |
|---|---|
| 모델 | `nano_banana_2` (Pro) |
| 비율 | 16:9 |
| 해상도 | 2K |
| output | 1/4 |
| Unlimited | ON |

```
1. media_upload(files: [ref_face.png, ref_product.png]) → upload_url 발급
2. PUT 업로드 → media_confirm → media_id 확정
3. generate_image({
     model: "nano_banana_2",
     prompt: 컷별 장면묘사 + 규칙0[A] + IMG_ENHANCE + GRADE,
     resolution: "2k",
     aspect_ratio: "16:9",
     output_count: 1,      # 1/4 output
     unlimited: true,      # Unlimited toggle ON
     medias: [
       {role: "image", value: face_media_id},
       {role: "image", value: product_media_id}
     ]
   }) × 30컷 → job_id 수집
4. 폴링·다운로드 → 백그라운드 에이전트에 위임 (8-동시 한도 준수)
5. 이미 디스크에 있으면 skip (resumable)
```

`COMMON` 구성: `규칙0[A] + IMG_ENHANCE + GRADE(막마다 다른 색 분위기 문자열)`  
컷마다 ref 조합을 다르게: 인물 컷=얼굴ref, 제품=제품ref, 둘 다 나오면 둘 다.

**항상 `run_in_background:true`로 실행**, 30컷 완료 후 알림.

> **CLI 경로 (30컷 일괄):** `higgsfield generate create nano_banana_2 --prompt "<규칙0[A]+IMG_ENHANCE+GRADE+장면>" --image <face.png> --image <product.png> --aspect_ratio 16:9 --resolution 2k --wait` × 셸 루프. 인물 일관성은 `soul-id create` → `--soul-id <ref_id>`. 결과 URL → `projects/{project}/{version}/images/`로 다운로드(`curl -o`/`Invoke-WebRequest -OutFile`).

> **Magnific 엔진으로 생성할 때:** ref 업로드(`creations_request_upload`→`creations_upload`→`creations_finalize_upload`) → `images_generate` → `creations_wait` → 다운로드. 규칙0·ENHANCE·새 버전 저장 동일.

### ⚠️ 에러 핸들링

> **시행착오 #8 → Higgsfield 기준:** `fetch failed` — 네트워크 일시 오류, 특정 컷에서 1~3회 날 수 있음 → 해당 컷만 재시도.

> **시행착오 #9 → 프로세스 강제 종료/중단:**
> 거대한 종료코드는 프로세스가 중간에 죽은 것. → 디스크에 실제 저장된 png를 확인하고, **빠진 컷만** 다시 생성한다.
> ```python
> jobs = [j for j in build_jobs() if not os.path.exists(SB + j[0] + ".png")]  # 없는 것만
> ```

> **Higgsfield 고유 에러:**
> - **프리셋 추천 차단**(nsfw/ip_detected 오탐으로 제출 안 됨): `declined_preset_id`(추천된 preset id)를 params에 넣어 리터럴 생성 강제.
> - **nsfw/ip_detected 오탐**: 무해한 컷에서도 발생 → 표현 순화 후 재시도. 해결 안 되면 다른 엔진/버전 이미지 교체.
> - **실패 컷만 재시도**: 성공분은 건드리지 않고 빠진 것만 재제출.

---

## 🚪 GATE 10 — 인터랙티브 스토리보드 HTML 빌드 & 인라인 수정

### 🏗️ HTML 조립 (`system_v2/_build_{name}_embed.py`)
- 각 png를 **Pillow로 width 760 리사이즈 → JPEG q82 → base64**로 박아 **자체완결 HTML 1파일**을 만든다(외부 이미지 의존 없음).
- 컷마다 카드: 썸네일 + 번호 + 막 태그 + 한글 장면 + 제품 역할 (결정적 순간 ★컷은 카마인 하이라이트).
- HTML에 **인터랙티브 리뷰 패널이 내장**된다 — 카드 클릭 시 우측에서 슬라이드인.
- 출력 파일은 **반드시 그 버전 폴더 안** `preview/`에 저장. (`storyboard_{NAME}_30cut_v{날짜}.html`)

### 🖥️ 리뷰 서버 실행 (필수 — file://로 열지 말 것)

```bash
# HTML 빌드 후 반드시 이 방식으로 접속
python3 system_v2/_review_server.py --project {PROJECT} --version {VERSION} [--port 7800]
# → 브라우저가 http://localhost:7800 자동 오픈
# → 서버가 HTML을 서브하므로 fetch('/api/regenerate') 정상 동작
```

> **⚠️ file://로 직접 열면 Chrome이 localhost fetch를 차단해 리뷰 기능이 동작하지 않는다.**
> HTML에 황색 배너가 표시되며 서버 링크가 안내된다.

### 🔁 인라인 수정 워크플로우

1. 리뷰 서버 실행 후 `http://localhost:7800` 접속
2. 수정할 카드 **클릭** → 우측 리뷰 패널 슬라이드인
3. 패널에서 선택:

| 컨트롤 | 이미지 옵션 | 영상 옵션 |
|---|---|---|
| 타입 | 🖼 이미지 | ▶ 영상 |
| 모델 | nano_banana_2(기본) / flux_2 / seedream_v4_5 / gpt_image_2 / flux_kontext | kling3_0_turbo(기본) / kling3_0 / seedance_2_0 / seedance_2_0_mini / veo3 |
| 해상도 | 1k / 2k(기본) / 4k | — |
| 길이 | — | 3 / 4 / 5(기본) / 8초 |
| 화질 | — | 720p / 1080p(기본) |

4. 수정 요청 입력 → **Enter** (Shift+Enter = 줄바꿈)
5. 서버가 `higgsfield generate create <model> --wait --json` 실행 → 완료 시 카드 썸네일 자동 교체

### 🛠️ 리뷰 서버 구조 (`system_v2/_review_server.py`)

- **포트**: 7800 (충돌 시 `--port` 인자로 변경)
- **엔드포인트**: `POST /api/regenerate` → CLI 실행 → 이미지는 base64, 영상은 `/api/videos/` URL로 응답
- **저장 경로**: 이미지 → `assets/images/cut_XX_v1.png`, `_v2.png` … (버전 누적, 덮어쓰기 금지), 영상 → `assets/videos/cut_XX_v1.mp4`, `_v2.mp4` … (원본 `cut_XX.png`/`cut_XX.mp4` 보존)
- **CLI 커맨드 형식** (파라미터명은 언더스코어):
  ```bash
  # 이미지
  higgsfield generate create nano_banana_2 --prompt "..." --aspect_ratio 16:9 --resolution 2k --wait --json
  # 영상
  higgsfield generate create kling3_0_turbo --prompt "..." --aspect_ratio 16:9 --duration 5 --resolution 1080p --wait --json
  ```

### ❓ Q10-1. 인라인 수정 후 처리 방식
- A. 수정 완료 컷만 교체, 나머지 유지 → G11 새 버전 필요 없이 진행 [기본]
- B. 수정 범위가 크다 → G11로 이동(새 버전 폴더)

> **시행착오 #10:** 생성 이미지를 에이전트가 Read로 열지 마라(컨텍스트 폭증 + 20MB 제한). 경로만 안내하고 사람이 본다.

---

## 🚪 GATE 11 — 수정 = 새 버전 (덮어쓰기 절대 금지)

> **시행착오 #11:** 수정이 있을 때마다 덮어쓰지 말고 폴더와 html 파일을 버전으로 나누어 계속 추가.

수정 요청이 오면:
1. **새 버전 폴더** 생성: `projects/{name}/v{날짜}_v2` (다음은 `_v3`…).
2. **안 바뀐 컷은 복사**, 바뀐 컷만 새로 생성.
3. HTML은 버전 접미사를 달아 **그 폴더 안에** 저장.
4. build 스크립트는 폴더 경로를 환경변수/상수로 분리해 버전마다 갈아끼운다.
5. 이전 버전(v1~)은 **그대로 보존**.

### ❓ Q11-1. 이번 수정 범위는? (객관식)
- A. 특정 컷 몇 개만 / B. 특정 막부터 뒤 전부 / C. 컨셉 자체(→ GATE 2~3부터 다시) / D. 미술·색만 전체 보정
