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

**우선순위:** 규칙0 [A][B] > IMG_ENHANCE/VID_ENHANCE > 유형별 확장 상수.  
충돌 시 규칙0이 항상 이긴다.

> **`gpt_image_2` 프롬프트 작성:** `--prompt` 본문은 `gpt-image-prompt` 스킬(Scene/Subject/Important details/Use case/Constraints 5단 구조 + 안티슬롭 규칙 — "stunning" 대신 구체적 시각 정보, 텍스트는 따옴표+폰트 명시)을 적용해 작성한다. 위 우선순위표보다 하위 — 규칙0·`IMG_ENHANCE`/`IMG_ENHANCE_OBJECT`와 충돌 시 그쪽이 이긴다. (인물/얼굴 ref 컷에는 여전히 쓰지 않음 — 부록 E #21.)

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

> **적용 위치:** GATE 8 프리뷰에 **"규칙 0 MANDATORY 프리픽스 + 강화 상수 주입됨"** 표기 / GATE 9 이미지 `COMMON += 규칙0[A] + IMG_ENHANCE` / GATE 12 영상 프롬프트 = **`규칙0[B](No BGM·SFX only)` 를 맨 앞에 두고** `+= VID_ENHANCE`. 컷별 추천 영상 프롬프트(`video_prompts.json`)에도 **맨 앞 줄에 No-BGM/SFX-only**를 박고 컷 상황에 맞는 카메라 무브를 미리 넣어둔다.

---

## 3) IMG_ENHANCE_OBJECT — 제품/오브제·무인물 컷 (부록 F-7)

```text
CINEMATIC PHOTOREAL OBJECT — REQUIRED ENHANCEMENT (append to every object/macro image prompt):
A real frame from a premium luxury TV commercial — never CGI / 3D-render / illustration. Material realism, no people, no faces.
ABSOLUTELY NO front-facing, NO eye-level framing. Use ONLY extreme LOW-ANGLE (camera on the floor looking steeply UP, subject looms overhead, upward foreshortening, converging verticals), extreme HIGH-ANGLE top-down, or DUTCH-ANGLE (20-40° roll). Off-center, artistic composition with negative space — never honest centered framing.
LENS LOGIC: if wide-angle → push visible BARREL DISTORTION (verticals bow, edges stretch); if telephoto → ULTRA-shallow depth of field, razor-thin plane of focus, telephoto background compression, creamy bokeh (only a sliver sharp).
LIGHTING: single hard sculpted BACKLIGHT / rim-light; black NEGATIVE FILL on the shadow side (one side into deep controlled shadow); gorgeous dramatic light with strong color contrast and balance; LOW-KEY only, never high-key, no blown highlights.
CAMERA/LENS FEEL: shot on ARRI Alexa 65 with vintage anamorphic lens; gentle filmic SOFTNESS — NOT clinical digital sharpness; heavy organic 35mm film grain (Vision3 500T +1 stop); Black Pro-Mist halation bloom on highlights; anamorphic oval bokeh + horizontal lens flare; crushed blacks, high-contrast chiaroscuro.
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
CAMERA/LENS FEEL: shot on ARRI Alexa with a vintage anamorphic lens; gentle filmic SOFTNESS — NOT clinical digital sharpness; heavy organic 35mm film grain (Vision3 500T); Black Pro-Mist halation bloom; anamorphic oval bokeh + horizontal flare; crushed blacks, low saturation.
Frame as a keyframe primed for dynamic fast video motion with a built-in match-cut out-point.
```

---

## 5) VID_ENHANCE_SFX — 인물 영상 프롬프트 맨 앞에 합침 (부록 H-6)

```text
AUDIO (TOP PRIORITY): diegetic sound effects ONLY — absolutely NO background music, NO BGM, NO musical score, NO singing. Only real SFX (rain, footsteps, neon buzz, whoosh, impact, electric hum).
MOTION: every clip carries deliberate DYNAMIC camera movement chosen per cut + a MATCH-CUT link to the adjacent cut. NO static locked-off shots. Relentless fast TV-CF tempo in the @cheonghhhhhhhhh reference grammar; ARRI low-saturation filmic look, magenta/cyan neon practicals, motion blur, match-cut continuity carrying motion across cuts.
```

---

## 6) VID_ENHANCE_OBJECT — 제품/오브제·매크로 영상 (부록 I-5)

```text
DYNAMIC MOTION OBJECT — REQUIRED (the AUDIO line MUST be the FIRST line):
AUDIO (TOP PRIORITY): diegetic SFX ONLY — absolutely NO background music, NO BGM, NO musical score. Only a few diegetic SFX fitting the shot (pour splash, ember crackle, metal scrape, wind, low whoosh). NO musical bed.
MOTION: relentless, continuously-accelerating dynamic move per cut — FPV forward dive (dutch roll), fast macro plunge into micro-detail, high-velocity orbit, speed-ramp (slow-mo → fast snap), whip-pan. Heavy motion-blur streaks; one consistent direction so a sub-second beat can be trimmed.
LIGHTING: gorgeous dramatic hard backlight, anamorphic flare, halation bloom (lighting-driven, glamorous).
OUT-POINT: end as a surface / light source / texture fills and SWALLOWS the frame — a built-in match-cut hand-off to the next shot.
Keep the start image's ARRI Alexa + anamorphic, soft-not-clinical, heavy-film-grain look. NO music — SFX only.
```
