# 03_reference_enhance-prompts.md — 생성 직전 로드 (상수 라이브러리)

> 이미지·영상 생성 직전에 이 파일을 로드해 해당 상수를 프롬프트에 주입한다.  
> 규칙0 [A][B]와 ENHANCE 상수는 **VERBATIM(글자 그대로)**이며 임의로 수정하지 않는다.

---

## 어떤 상수를 언제 쓰나 (선택 가이드)

| 유형 | 이미지 상수 | 영상 상수 |
|---|---|---|
| **인물 광고** (주인공 얼굴 등장하는 컷) | `IMG_ENHANCE_PERSON` (G-5) | `VID_ENHANCE_SFX` (H-6) |
| **제품·오브제 광고** (인물 얼굴 없음, 손·실루엣·제품·환경) | `IMG_ENHANCE_OBJECT` (F-7) | `VID_ENHANCE_OBJECT` (I-5) |
| **공통 기본** (모든 컷 기본 적용) | `IMG_ENHANCE` | `VID_ENHANCE` |
| **캐릭터 1차 레퍼런스 학습** (사진 5장 이상) | `SOUL_CHARACTER_TRAINING`(섹션 7, Higgsfield `show_characters` + `soul_2` — 규칙0[A] 미적용) | — |
| **캐릭터 턴어라운드 시트** (사진 5장 미만일 때 대체) | `CHAR_TURNAROUND_SHEET`(섹션 7b, `gpt_image_2` 전용, 레거시 — 규칙0[A] 미적용) | — |

**우선순위:** 규칙0 [A][B] > `CAMERA_LOOK`(공통 카메라·렌즈·룩·금지 미감) > IMG_ENHANCE/VID_ENHANCE > 유형별 확장 상수.  
충돌 시 규칙0이 항상 이긴다.

> **영상 상수(`VID_ENHANCE`/`VID_ENHANCE_SFX`/`VID_ENHANCE_OBJECT`) 적용 방법:** 영상 프롬프트는 `VIDEO_PROMPT_FORMAT`(2b, 700자 캡)로 작성하므로 위 표의 영상 상수 텍스트를 통째로 붙이지 않는다 — 요구사항만 SHOT GROUP/LIGHT/SFX 필드에 녹여 쓴다(상세는 2b).

> **`gpt_image_2` 프롬프트 작성:** `--prompt` 본문은 `gpt-image-prompt` 스킬(Scene/Subject/Important details/Use Case & Constraints 4단 구조 + 안티슬롭 규칙 — "stunning" 대신 구체적 시각 정보, 텍스트는 따옴표+폰트 명시)을 적용해 작성한다. 위 우선순위표보다 하위 — 규칙0·`IMG_ENHANCE`/`IMG_ENHANCE_OBJECT`와 충돌 시 그쪽이 이긴다. (인물/얼굴 ref 컷에는 여전히 쓰지 않음 — 부록 E #21.)

---

## 규칙 0 — 이미지·영상 생성 시 무조건·강제 (NON-NEGOTIABLE)

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

---

## CAMERA_LOOK — 공통 카메라·렌즈·룩 레퍼런스 (이미지·영상 공통, VERBATIM)

> 아래는 **모든 이미지/영상 프롬프트의 카메라·렌즈·색·그레인·레퍼런스 감독·금지 미감**의 단일 기준이다. `IMG_ENHANCE_OBJECT`·`IMG_ENHANCE_PERSON`·`VID_ENHANCE_SFX`·`VID_ENHANCE_OBJECT`의 "CAMERA/LENS FEEL" 줄은 이 블록을 가리키며, 컷 유형별 추가 디테일(역광 종류·바운스·아웃포인트 등)만 그 절에서 보충한다. 이전에 절마다 따로 적혀 있던 "ARRI Alexa 65" / "ARRI Alexa" 표기 불일치는 이 블록으로 통일한다.

```text
CAMERA:    ARRI ALEXA Mini LF
LENS:      ZEISS Master Prime (24mm-100mm)
ASPECT:    anamorphic 2.39:1
COLOR:     ARRI K1S1 LogC + custom Show LUT
GRAIN:     Kodak Vision3 500T (medium-heavy)
REFERENCE: Denis Villeneuve × David Fincher × Park Chan-wook
NEGATIVE:  NEVER Chinese-aesthetic, NEVER over-saturated,
           NEVER cartoonish, NEVER K-pop MV gloss
```

> **우선순위:** 규칙0 [A][B] > `CAMERA_LOOK` > `IMG_ENHANCE`/`VID_ENHANCE` > 유형별 확장 상수. NEGATIVE 줄은 모든 이미지·영상 프롬프트에 공통 적용(인물·오브제·영상 구분 없음).

---

## 1) IMG_ENHANCE — 이미지 강화 (모든 이미지 컷 공통)

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

---

## 2) VID_ENHANCE — 영상 강화 (모든 영상 컷 공통)

의도(한글): **① 오디오는 무조건 BGM 없이 효과음(SFX)만**(가장 강한 고정 규칙 — 규칙 0 [B] 참조, BGM·내레이션은 후반 합성) / ② 컷 상황에 맞게 핸드헬드·dolly in·arc·로봇암 등 **다이내믹 무브먼트를 반드시** 넣고 컷 간 매치컷/트랜지션으로 연결. (단, 크로마키 플레이트 영상은 키잉을 위해 **locked-off 고정 카메라** 예외 — 부록 E 참조.)

```text
DYNAMIC MOTION — REQUIRED ENHANCEMENT (the audio line MUST be first on every video prompt):
No background music. NO BGM. NO score. SFX only — at most a few subtle diegetic sound effects; no musical bed whatsoever.
Every clip MUST carry deliberate dynamic camera movement chosen to fit the cut — handheld energy, dolly / push-in, arc / orbit, crane-up / pull-up, ROBOT-ARM dynamic sweep, crash-zoom, tilt-up, over-the-shoulder telephoto. (EXCEPTION: chroma-green plate clips stay LOCKED-OFF static for clean keying — only the subject moves.)
Write a real moving-shot keyframe (mid-action + motion blur), and add a match-cut / transition link to the adjacent cut.
```

> **적용 위치:** GATE 8 프리뷰에 **"규칙 0 MANDATORY 프리픽스 + 강화 상수 주입됨"** 표기 / GATE 9 이미지 `COMMON += 규칙0[A] + IMG_ENHANCE` / GATE 12 영상 프롬프트 = **`규칙0[B](No BGM·SFX only)` 를 맨 앞에 두고**, 아래 `VIDEO_PROMPT_FORMAT`(2b) 7필드 구조로 채우며 `VID_ENHANCE`의 요구사항(다이내믹 무브먼트·매치컷 연결)은 SHOT GROUP 비트 안에 녹여 쓴다(700자 캡 — 텍스트 블록 통째 결합 금지, 상세는 2b 참조). 컷별 추천 영상 프롬프트(`video_prompts.json`)에도 **맨 앞 줄에 No-BGM/SFX-only**를 박고 컷 상황에 맞는 카메라 무브를 미리 넣어둔다.

---

## 2b) VIDEO_PROMPT_FORMAT — 영상 프롬프트 표준 필드 순서 (Hailuo 2.3 기본·Seedance 2.0 백업 공통, 700자 이내)

> 모든 `[video prompt]`(scenario.md) / GATE 12 실제 호출 프롬프트는 규칙0[B](No-BGM 한 줄, 최상단 고정) 다음에 아래 7개 필드를 **이 순서 그대로** 채워 한 문단으로 합친다. **전체 길이는 공백 포함 700자를 넘지 않는다** — 넘으면 SHOT GROUP 세부 비트 묘사를 줄여서 맞춘다(규칙0[B]·RUNTIME·CAMERA는 줄이지 않음). CAMERA에 렌즈/아나모픽 비율을 한 줄로 합치고(LENS·LOOK 별도 줄 없음, 디테일은 `CAMERA_LOOK` 공통 블록 참조), SHOT은 6초 러닝타임 내부를 **BEGINS WITH → ACTION → TRANSITION → ENDS WITH** 타임스탬프 비트로 쪼개 미니 시퀀스로 적는다. (백업 Seedance 2.0으로 생성할 때는 RUNTIME/SHOT GROUP 합을 5초로 다시 맞춘다.)

```text
[규칙0[B] No-BGM/SFX-only 한 줄 — 항상 최상단, 고정]
RUNTIME: 6 seconds.
CAMERA: ARRI ALEXA Mini LF, ZEISS, anamorphic 2.39:1.
TIME: [장면 시간대 — 예: deep midnight 03:14 AM, dusk, overcast noon]

CHARACTER: [이름 — 머리·눈·입술·의상 등 식별 키워드 한 줄, 오브제 컷이면 생략]

SHOT GROUP — 6 SECOND SEQUENCE:
BEGINS WITH (0:00-0:01): [시작 동작]
ACTION (0:01-0:04): [핵심 동작]
TRANSITION (0:04-0:05): [전환 동작]
ENDS WITH (0:05-0:06): [마무리 동작/매치컷 아웃포인트]

LIGHT: [조명 한 줄 — 백라이트/네거티브 필 등]
SFX: [디제틱 효과음 — 예: tar-paper footsteps, *KNOCK-KNOCK* signature]
```

**예시 (약 620자, 700자 이내):**
```text
RUNTIME: 6 seconds.
CAMERA: ARRI ALEXA Mini LF, ZEISS, anamorphic 2.39:1.
TIME: deep midnight 03:14 AM.

CHARACTER: JION — auburn medium wavy bob,
blue-grey eyes, vivid red lips, black blazer.

SHOT GROUP — 6 SECOND SEQUENCE:
BEGINS WITH (0:00-0:01): JION steps onto rooftop.
ACTION (0:01-0:04): She walks toward central skylight
with tactical purpose. Boots on tar-paper roof.
TRANSITION (0:04-0:05): She crouches at skylight edge.
ENDS WITH (0:05-0:06): Macro on her finger as she
KNOCKS twice — *KNOCK-KNOCK*.

LIGHT: deep midnight + red glow from skylight.
SFX: tar-paper footsteps, *KNOCK-KNOCK* signature.
```

> RUNTIME은 #40(2026-06-22부터 기본 6초 고정, Hailuo 2.3) 그대로 — 절대 다른 값으로 바꾸지 않는다. SHOT GROUP의 4비트(0:00-0:01 / 0:01-0:04 / 0:04-0:05 / 0:05-0:06) 합은 항상 6초여야 한다. 700자 카운트는 규칙0[B] 줄을 포함한 전체 합산. (백업 Seedance 2.0 사용 시에는 5초·구버전 4비트 분배로 되돌린다.)

> **`VID_ENHANCE`/`VID_ENHANCE_SFX`/`VID_ENHANCE_OBJECT`와의 관계(충돌 방지):** 이 세 상수는 그 자체로 400~700자 분량의 별도 텍스트 블록이라, 700자 캡과 함께 **문자 그대로 이어붙이면 즉시 캡을 초과**한다. 영상 프롬프트에서는 이 상수들을 **요구사항 체크리스트로만** 쓴다 — "다이내믹 무브먼트 필수·매치컷 연결·locked-off 금지(크로마키 예외)" 같은 지시는 위 SHOT GROUP의 각 비트(BEGINS WITH/ACTION/TRANSITION/ENDS WITH)에 직접 녹여 쓰고, "SFX-only" 지시는 규칙0[B](항상 최상단)로 이미 충족되므로 SFX 필드에는 실제 효과음 내용만 적는다. **세 상수의 텍스트 블록을 통째로 추가 결합하지 않는다.** (이미지 프롬프트의 `IMG_ENHANCE`/`IMG_ENHANCE_PERSON`/`IMG_ENHANCE_OBJECT`는 700자 캡이 없으므로 그대로 문자 그대로 결합 — 이 예외는 영상에만 적용.)

---

## 3) IMG_ENHANCE_OBJECT — 제품/오브제·무인물 컷 (부록 F-7)

```text
CINEMATIC PHOTOREAL OBJECT — REQUIRED ENHANCEMENT (append to every object/macro image prompt):
A real frame from a premium luxury TV commercial — never CGI / 3D-render / illustration. Material realism, no people, no faces.
ABSOLUTELY NO front-facing, NO eye-level framing. Use ONLY extreme LOW-ANGLE (camera on the floor looking steeply UP, subject looms overhead, upward foreshortening, converging verticals), extreme HIGH-ANGLE top-down, or DUTCH-ANGLE (20-40° roll). Off-center, artistic composition with negative space — never honest centered framing.
LENS LOGIC: if wide-angle → push visible BARREL DISTORTION (verticals bow, edges stretch); if telephoto → ULTRA-shallow depth of field, razor-thin plane of focus, telephoto background compression, creamy bokeh (only a sliver sharp).
LIGHTING: single hard sculpted BACKLIGHT / rim-light; black NEGATIVE FILL on the shadow side (one side into deep controlled shadow); gorgeous dramatic light with strong color contrast and balance; LOW-KEY only, never high-key, no blown highlights.
CAMERA/LENS FEEL (CAMERA_LOOK 공통 블록 적용): ARRI ALEXA Mini LF + ZEISS Master Prime (24-100mm), anamorphic 2.39:1, ARRI K1S1 LogC + custom Show LUT, Kodak Vision3 500T grain (medium-heavy, +1 stop on this object/macro cut); gentle filmic SOFTNESS — NOT clinical digital sharpness; Black Pro-Mist halation bloom on highlights; anamorphic oval bokeh + horizontal lens flare; crushed blacks, high-contrast chiaroscuro. NEGATIVE: NEVER Chinese-aesthetic, NEVER over-saturated, NEVER cartoonish, NEVER K-pop MV gloss.
Compose as a keyframe primed for dynamic fast video motion (match-cut out-point built in).
```

---

## 4) IMG_ENHANCE_PERSON — 인물 컷 공통 (부록 G-5)

```text
CINEMATIC PHOTOREAL PERSON — REQUIRED ENHANCEMENT (append to every hero/person image prompt):
A real frame from a premium TV commercial — never CGI / 3D-render / video-game / AI render. Flawless photoreal skin micro-texture; a sophisticated, refined, good-looking subject.
IDENTITY LOCK: exactly the SAME man as the reference (same face, age, hairstyle) — do NOT alter the face.
ABSOLUTELY NO front-facing, NO honest eye-level framing; the subject never stares into the lens. Use ONLY extreme LOW-ANGLE (worm's-eye looking up), extreme HIGH-ANGLE top-down, or DUTCH-ANGLE; off-center stylish composition with negative space.
LENS LOGIC: wide-angle → visible BARREL distortion (subject can loom close to the lens); telephoto → ULTRA-shallow demai depth of field + background compression + creamy bokeh (only a sliver sharp).
LIGHTING: single hard sculpted BACKLIGHT / rim-light with black NEGATIVE FILL on the shadow side; low-key chiaroscuro; magenta/cyan motivated practicals; never high-key, no blown highlights.
CAMERA/LENS FEEL (CAMERA_LOOK 공통 블록 적용): ARRI ALEXA Mini LF + ZEISS Master Prime (24-100mm), anamorphic 2.39:1, ARRI K1S1 LogC + custom Show LUT, Kodak Vision3 500T grain (medium-heavy); gentle filmic SOFTNESS — NOT clinical digital sharpness; Black Pro-Mist halation bloom; anamorphic oval bokeh + horizontal flare; crushed blacks, low saturation. NEGATIVE: NEVER Chinese-aesthetic, NEVER over-saturated, NEVER cartoonish, NEVER K-pop MV gloss.
Frame as a keyframe primed for dynamic fast video motion with a built-in match-cut out-point.
```

---

## 5) VID_ENHANCE_SFX — 인물 영상 요구사항 체크리스트 (부록 H-6)

> **영상 프롬프트(700자 캡)에는 아래 텍스트를 통째로 붙이지 않는다** — 2b `VIDEO_PROMPT_FORMAT`의 SHOT GROUP/LIGHT/SFX 필드에 요구사항만 녹여 쓴다. 아래 텍스트는 다른 영상 엔진/용도(예: 풀텍스트 프롬프트가 허용되는 경우)를 위한 레퍼런스 원문이다.

```text
AUDIO (TOP PRIORITY): diegetic sound effects ONLY — absolutely NO background music, NO BGM, NO musical score, NO singing. Only real SFX (rain, footsteps, neon buzz, whoosh, impact, electric hum).
MOTION: every clip carries deliberate DYNAMIC camera movement chosen per cut + a MATCH-CUT link to the adjacent cut. NO static locked-off shots. Relentless fast TV-CF tempo in the @cheonghhhhhhhhh reference grammar; CAMERA_LOOK 공통 블록(ARRI ALEXA Mini LF + ZEISS Master Prime, low-saturation filmic look) 유지, magenta/cyan neon practicals, motion blur, match-cut continuity carrying motion across cuts. NEGATIVE: NEVER Chinese-aesthetic, NEVER over-saturated, NEVER cartoonish, NEVER K-pop MV gloss.
```

---

## 6) VID_ENHANCE_OBJECT — 제품/오브제·매크로 영상 요구사항 체크리스트 (부록 I-5)

> **영상 프롬프트(700자 캡)에는 아래 텍스트를 통째로 붙이지 않는다** — 2b `VIDEO_PROMPT_FORMAT`의 SHOT GROUP/LIGHT/SFX 필드에 요구사항만 녹여 쓴다. 아래 텍스트는 레퍼런스 원문이다.

```text
DYNAMIC MOTION OBJECT — REQUIRED (the AUDIO line MUST be the FIRST line):
AUDIO (TOP PRIORITY): diegetic SFX ONLY — absolutely NO background music, NO BGM, NO musical score. Only a few diegetic SFX fitting the shot (pour splash, ember crackle, metal scrape, wind, low whoosh). NO musical bed.
MOTION: relentless, continuously-accelerating dynamic move per cut — FPV forward dive (dutch roll), fast macro plunge into micro-detail, high-velocity orbit, speed-ramp (slow-mo → fast snap), whip-pan. Heavy motion-blur streaks; one consistent direction so a sub-second beat can be trimmed.
LIGHTING: gorgeous dramatic hard backlight, anamorphic flare, halation bloom (lighting-driven, glamorous).
OUT-POINT: end as a surface / light source / texture fills and SWALLOWS the frame — a built-in match-cut hand-off to the next shot.
Keep the start image's CAMERA_LOOK 공통 블록(ARRI ALEXA Mini LF + ZEISS Master Prime, anamorphic 2.39:1) look — soft-not-clinical, heavy Kodak Vision3 500T grain. NO music — SFX only. NEGATIVE: NEVER Chinese-aesthetic, NEVER over-saturated, NEVER cartoonish, NEVER K-pop MV gloss.
```

---

## 7) SOUL_CHARACTER_TRAINING — 캐릭터 1차 레퍼런스 학습 (Higgsfield Soul, 기본값, 부록 E #39)

> **언제 쓰나:** 주인공 얼굴 ref가 아직 없고, 사용자가 실사 사진 5~20장을 제공할 때. 이걸로 재사용 가능한 Soul Character(identity model, `soul_id`)를 학습해 이후 모든 개별 컷(`nano_banana_2`)의 identity-lock 기준 이미지를 뽑는 데 쓴다. **이제 기본값** — 사진이 5장 이상 있으면 아래 7b의 `gpt_image_2` 턴어라운드 시트보다 이쪽을 먼저 쓴다.
> **모델 제약(중요):** 학습된 `soul_id`는 **`soul_2`(Soul V2)·`soul_cinema_studio`로만** 생성 가능하다. 개별 스토리보드 컷 생성은 여전히 `nano_banana_2`로 통일(부록 E #38 — soul_2 미사용 정책 그대로 유지). 즉 Soul 학습은 **1차 얼굴 레퍼런스 스틸(`ref_face.png`)을 만드는 용도로만** 쓰고, 그 결과 이미지를 이후 `nano_banana_2` 컷 생성에 medias로 첨부한다 — soul_id 자체를 컷 생성에 직접 쓰지 않는다.
> **캐릭터 동결(재사용) 정책:** 같은 인물을 여러 프로젝트에서 쓸 때는 `soul_id`를 **한 번만 발급하고 재사용**한다 — 프로젝트마다 재학습하지 않는다. 외형(헤어·의상 등)이 달라져도 동일 인물이면 같은 `soul_id`를 그대로 쓰고 프롬프트로 외형만 바꾼다. 새 인물일 때만 새로 학습한다.

### 학습용 사진 체크리스트 (5장 이상, 진행 전 필수 확인)
- **장수:** 최소 5장 (5~20장 범위 권장).
- **각도:** 정면 + 측면 + 3/4 등 **다양한 각도**를 섞는다 — **전부 같은 각도 금지**.
- **표정:** 미소 + 응시(무표정) 등 **다양한 표정**을 섞는다.
- **조명 톤:** 5장 전체가 **같은 조명 톤**이어야 한다 — 극단적으로 다른 조명(역광 vs 정면광 등) 혼재 금지.
- **해상도:** 장당 **최소 1024×1024**.
- **동일 인물:** 5장 모두 **같은 사람**이어야 한다 — 다른 사람 사진 섞지 않는다.
- **선명도:** 흐릿하거나 초점이 안 맞은 사진은 쓰지 않는다.
- 위 기준 중 하나라도 불충족(특히 5장 미만·다른 인물 혼재·흐릿함)이면 학습을 진행하지 말고 사용자에게 재촬영/재선별을 요청한다.

### 저장 위치 — 전역 레지스트리 + 프로젝트별 포인터
- **전역 레지스트리(1회 학습, 모든 프로젝트 공유):** `assets/character_refs/{name}/`
  - `assets/character_refs/{name}/*.jpg` — 학습용 원본 사진 5~20장
  - `assets/character_refs/{name}/character.json` — `{ name, soul_id, type: "soul_2", trained_at, source_images: [...] }`
- **프로젝트별 포인터(재학습 없이 동결된 ID 참조):** `projects/{project}/{version}/ref/`
  - `projects/{project}/{version}/ref/{name}_character.json` — 레지스트리의 `character.json`을 그대로 복사한 포인터(soul_id 동일, 재학습 금지)
  - `projects/{project}/{version}/ref/ref_face_v1.png` — 그 `soul_id`로 이 프로젝트용으로 뽑은 1차 얼굴 레퍼런스 스틸(이후 `nano_banana_2` 컷의 identity-lock 기준)
  - (구 변형 위치 `images/ref/`, `keyvisual/`는 신규 프로젝트에 쓰지 않음 — `ref/`로 통일.)

### 진행 순서
1. 사용자가 `assets/character_refs/{name}/`에 위 **학습용 사진 체크리스트**를 만족하는 사진 5~20장을 넣는다. **이미 같은 인물의 `character.json`이 있으면 학습을 건너뛰고 그 `soul_id`를 재사용**한다.
2. 받은 사진이 체크리스트를 만족하는지 확인한다(장수·각도 다양성·표정 다양성·조명 일관성·해상도·동일 인물·선명도) — 불충족 항목이 있으면 1로 돌아가 사용자에게 재요청.
3. 각 사진을 `media_upload`로 presigned URL 발급 → 바이트 PUT → `media_confirm`으로 `media_id` 확보.
4. `show_characters({action: "train", name: "{name}", images: [media_id, ...]})` 호출 — 학습은 비차단(약 10분), 도구가 폴링.
5. `show_characters({action: "status", soul_id})`로 `ready` 확인.
6. `soul_id`를 `assets/character_refs/{name}/character.json`(레지스트리)과 `projects/{project}/{version}/ref/{name}_character.json`(포인터) 양쪽에 저장.
7. `generate_image({model: "soul_2", params: {soul_id, prompt: "..."}})`로 레퍼런스 스틸 1장을 뽑아 `projects/{project}/{version}/ref/ref_face_v1.png`로 저장 — 이후 개별 컷(`nano_banana_2`)의 identity-lock 기준 이미지로 쓴다.

```
show_characters({ action: "train", name: "JUNE", images: [...5개 media_id] })
  → soul_id 발급, assets/character_refs/JUNE/character.json + projects/{project}/{version}/ref/JUNE_character.json에 저장

generate_image({ model: "soul_2", params: { soul_id, prompt: "..." } })
  → projects/{project}/{version}/ref/ref_face_v1.png
```

---

## 7b) CHAR_TURNAROUND_SHEET — 캐릭터 턴어라운드 레퍼런스 시트 (gpt_image_2 전용, 레거시 — 부록 E #37 재사용 템플릿)

> **언제 쓰나:** 학습용 사진이 5장 미만이라 위 7번 Soul 학습을 쓸 수 없을 때의 대체 경로. 1차 키비주얼로 멀티패널 턴어라운드 시트를 만들어 이후 모든 개별 컷(`nano_banana_2`)의 identity-lock 기준으로 삼는다.
> **모델 고정:** `gpt_image_2`만 쓴다 — `soul_2`는 `enhance_prompt` 강제로 멀티패널 구도 지시를 단일컷으로 재작성해버려 패널 구조가 무시된다(#37).
> **규칙0[A]와의 관계:** 이 시트는 정면 뷰가 정의상 필수(턴어라운드 목적)이므로 규칙0[A]의 "정면·아이레벨 금지"는 **이 시트에는 적용하지 않는다**. 시트에서 좋은 컷을 골라 실제 광고 컷을 생성할 때는 규칙0[A]+IMG_ENHANCE_PERSON을 그대로 적용한다.

```text
A professional character reference sheet based strictly on the reference identity. Two rows on a clean neutral plain light-grey background.
TOP ROW: four full-body standing views in a relaxed A-pose — front, left profile, right profile, back — consistent scale and alignment, accurate anatomy.
BOTTOM ROW: three close-up portraits — front, left profile, right profile — showing a gentle warm smile, clear bright lively eyes, soft features.
Maintain perfect identity consistency across every panel. Consistent soft even lighting across all panels.
Crisp, ultra-realistic, print-ready character sheet, 16:9, soul cinematic style.
Subject: [주인공 외형 묘사 — 연령대·역할·의상·헤어·체형 등, 상표 없음].
```

```
generate_image({
  model: "gpt_image_2",
  prompt: CHAR_TURNAROUND_SHEET (위 템플릿의 [Subject] 자리만 교체),
  aspect_ratio: "16:9",
  resolution: "2k"
}) → projects/{project}/{version}/ref/ref_face_turnaround_v1.png
```

> **과거 사용 사례(구 경로):** energy-runner 프로젝트(20대 여성 마라톤 러너) — `projects/energy-runner/v20260621/keyvisual/ref_face_turnaround_v1.png`. (`keyvisual/`는 구 경로 표기, 신규 프로젝트는 `ref/`를 쓴다.)
