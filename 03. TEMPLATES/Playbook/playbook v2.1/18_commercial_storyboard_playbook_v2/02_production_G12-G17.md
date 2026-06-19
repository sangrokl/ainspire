# 02_production_G12-G17.md — 제작 단계 (GATE 12~17)

> 여기부터는 **베스트컷이 확정된 뒤**에 진행한다. 각 GATE는 독립적이라 필요한 것만 골라 써도 된다. 모든 외부 호출 전 GATE 8과 같은 **4종/설정 프리뷰 + 승인**을 지킨다.

> **BGM은 API로 자동생성하지 않는다** — GATE 13에서 에이전트가 Suno 프롬프트를 제안하고, 사용자가 [suno.com](https://suno.com)에서 직접 생성해 후반 조립에서 얹는다.

---

## GATE 12 — 영상화 (Seedance 2.0 · Higgsfield CLI/MCP · Magnific)

**왜:** 정지 스토리보드를 컷당 4초 움직이는 클립으로. "모든 영상에 다이내믹 무브먼트"가 들어가야 영상다워진다.

### Q12-1. 설정 (4종 + 승인)
| 항목 | 기본 |
|---|---|
| MODEL | CLI/Higgsfield MCP `seedance_2_0` 또는 Magnific `video_generate`(`video_models_list`로 모델 확인) |
| 해상도 | 1080p |
| 비율 | 16:9 |
| 길이 | 4초 (컷당 1개) |
| 오디오 | Seedance 2.0은 `generate_audio` 파라미터 없음 → 무음(영상 프롬프트 SFX 지시로 디제틱 사운드) |

- **비용 미리보기**: `generate_video(get_cost:true)` — 예) 4초·1080p = 36크레딧/컷 × 30 ≈ 1,080크레딧. `balance`로 잔액 확인 후 승인.

### Q12-2. 컷별 카메라 무브먼트 (상황에 맞게 배정 — TV CF 문법)
컷마다 **하나**를 명시: 핸드헬드 / 달리인·푸시인 / 아크·오빗 / 크레인업·풀업 / **로봇암 다이내믹 스윕** / 크래시줌 / 틸트업 / 오버숄더 망원. 정지 컷이 아니라 **"움직이는 샷의 키프레임"**으로 프롬프트를 쓴다(중간동작·모션블러). 앞 컷→뒤 컷 매치컷/트랜지션 연결고리도 프롬프트에 한 줄.

> **필수:** 모든 영상 프롬프트에 `03_reference_enhance-prompts.md`의 `VID_ENHANCE`를 합친다 — 컷 상황에 맞는 다이내믹 무브먼트(핸드헬드·dolly in·arc·로봇암 등) + 매치컷/트랜지션 연결 강제. 정지(locked-off) 샷 금지. 컷별 추천 무브는 `video_prompts.json`(GATE 17 영상전환 자동입력)에 미리 매핑.

> **규칙 0 [B] 강제:** 모든 영상 프롬프트 맨 앞에 `No background music. NO BGM. NO score. SFX only.` — 이 규칙은 어떤 상황에서도 약화되지 않는다.

### 실행 절차 (검증된 순서)
1. **업로드**: `media_upload(files[])`로 30컷 presigned URL 발급 → 각 PNG를 `urllib PUT`(또는 curl) → `media_confirm(media_ids[])`. (이미지 ≤1792×1008·4MB 확인. magnific 2K 업스케일본은 1080p jpg q92로 다운스케일 후 업로드.)
2. **생성**: 컷마다 `generate_video({model:'seedance_2_0', prompt(카메라무브 + VID_ENHANCE), duration:4, resolution:"1080p", aspect_ratio:"16:9", mode:"std", medias:[{role:"start_image", value:<media_id>}]})` → `job_id` 수집.
3. **폴링·다운로드는 메인에서 하지 말고 백그라운드 에이전트에 위임** — 8-동시 한도를 지키며 완료분을 받는 대로 `videos/seedance/{cut}.mp4`로 저장.

> **Higgsfield CLI로 영상화할 때 (업로드·폴링 자동):** 컷마다 `higgsfield generate create seedance_2_0 --prompt "<규칙0[B] No-BGM + 카메라무브 + VID_ENHANCE>" --start-image <컷이미지_경로_또는_jobID> --duration 4 --resolution 1080p --aspect_ratio 16:9 --wait`. `--start-image`가 업로드를 자동 처리(media TTL 신경 안 씀), `--wait`가 폴링까지 흡수해 Claude 토큰 0. 8-동시 한도는 셸에서 동시 실행 수로 조절. 비용 견적은 `higgsfield generate cost seedance_2_0 …`. 결과 URL은 `videos/seedance/{cut}.mp4`로 다운로드.

### 에러 핸들링 (실제로 겪음)
> **시행착오 #14 — 동시 8개 한도:** 플랜상 **max 8 concurrent jobs**. 9번째는 `Rate limit reached`. → 8개씩 큐로 돌리며 완료될 때마다 다음 제출. 이 반복은 백그라운드 에이전트가 관리.
> **시행착오 #15 — 프리셋 추천 안내:** 어두운 프롬프트는 `preset_recommendation`("IN THE DARK" 등) 안내를 띄우며 **제출이 안 된다**. → 같은 params에 `declined_preset_id`(추천된 preset id)를 넣어 **리터럴 생성 강제**.
> **시행착오 #16 — 콘텐츠 필터 오탐:** "rushes into his arms / hug / embrace" 같은 선의의 포옹 표현이 NSFW 오탐으로 막힌다. → 포옹 단어를 빼고 "two people standing close in a tender reunion, heavy winter clothing"처럼 우회.
> **시행착오 #17 — `fetch failed`:** 노드 fetch 일시 실패(네트워크/게이트웨이). 특정 컷에서 1~3회 날 수 있음 → 재시도.
> **media_id TTL:** 업로드 후 약 15분 내 제출. 만료 시 잡이 조용히 실패 → 재업로드 후 재제출.

**산출물:** `videos/seedance/halo_cNN.mp4` 30개 + 한 페이지 영상 리뷰 HTML(`<video autoplay muted loop>`).

> **→ 일괄 영상화 + 리뷰:** 확정 스토리보드를 **"전체 영상으로 돌리기"** 한 방으로 배치 생성하고, 끝나면 **GATE 17 영상 리뷰 콘솔**을 자동 팝업해 컷별로 초수·화질을 고르고 수정요청을 Enter로 보내 Seedance 2.0 재생성을 건다.

---

## GATE 13 — BGM (Suno 프롬프트 제안 → 사용자가 직접 생성)

**왜:** 30초 광고 음악. **API 자동생성은 하지 않는다**(CometAPI 등 키가 없을 수 있음). 대신 에이전트가 **Suno에 그대로 붙여넣을 프롬프트**를 만들어주고, 사용자가 [suno.com](https://suno.com)에서 직접 생성해 받는다. (영상 클립 자체는 규칙0[B]대로 SFX only — BGM은 후반 조립에서만 얹는다.)

### Q13-1. 음악 방향 (객관식)
| 선택 | 결 |
|---|---|
| A. 프리미엄·미니멀·세련 | 절제된 고급, 큰 드롭 없이 |
| B. 강렬·임팩트 | 묵직한 드롭, 공격적 |
| C. 트렌디·힙 | 글로벌 광고풍 |
| D. 웅장·시네마틱 | 영화 예고편 |

### Q13-2. 전개 구조 (객관식)
- A. 조용히→폭발(기승전결 또렷, 추천) / B. 처음부터 강하게 / C. 일정한 그루브

### 산출물 — Suno 붙여넣기용 프롬프트 (영어)
답을 받으면 아래를 반드시 갖춘 **영어 Suno 프롬프트**를 만들어 사용자에게 그대로 준다:
- **구체적 장르 + 레퍼런스 아티스트 + BPM** (제너릭 'EDM/house'는 금지 — 시행착오 #18)
- 악기·무드·구조(인트로→빌드→드롭/해소), 길이(30~60초 타깃), `instrumental` 여부
- 예) `Energetic premium drum & bass — live drums + analog bass + cinematic strings & brass, jazzy keys, 172 BPM, in the style of Netsky / Camo & Krooked; quiet intro building to one powerful impact drop; instrumental, polished commercial sound.`

### 사용자 안내 (그대로 전달)
1. 위 프롬프트 복사 → [suno.com](https://suno.com)에 붙여넣고 **Instrumental** 켜고 생성.
2. 나온 트랙에서 **베스트 30초 구간**을 골라 트림.
3. 그 mp3를 **최종 조립(GATE 16 / 부록 C-4)에서 A1(BGM) 트랙**으로 얹는다.

> **시행착오 #18:** 제너릭 EDM/하우스는 "스톡 광고음악 = 촌스러움". 정답은 **구체적 장르(예: DnB 기반) + 실악기 + 임팩트 + 레퍼런스 아티스트·BPM 명시.**

**산출물:** Suno 프롬프트 1개(영어) + 사용자 생성 안내. (생성된 mp3는 사용자가 받아 GATE 16에서 합성.)

---

## GATE 14 — 내레이션 VO (Higgsfield TTS 기본, ElevenLabs 대안)

**왜:** 영문 보이스오버. 스토리보드 비트에 맞춘 카피 + 톤에 맞는 성우.

### 준비: 엔진 선택
**기본 = Higgsfield TTS(`inworld_text_to_speech`).** Higgsfield 연결(STEP 0)만 있으면 OK, 별도 키·`.env` 불필요 — CLI `higgsfield generate create inworld_text_to_speech --prompt "..."` 또는 MCP `generate_audio`로 바로 생성.

**대안: ElevenLabs 직접 API.** (내레이션 = 선택 산출물, 이 경로 쓸 거면 키 필수)
`ELEVENLABS_API_KEY`가 `system_v2/.env`에 있어야 한다. **에이전트는 키를 대신 발급/OAuth할 수 없으므로**, 없으면 사용자에게 이렇게 안내한다:
1. `https://elevenlabs.io/app/settings/api-keys`에서 키 발급(무료 플랜 가능)
2. `system_v2/.env`를 열어 `ELEVENLABS_API_KEY=` 뒤에 키 붙여넣기 (파일은 이미 있음)
3. `node system_v2/check_api_connections.mjs`로 확인 (`ElevenLabs: OK`면 됨)

`GET /v1/voices`로 동작 확인 + 보이스 목록 확보(ElevenLabs 경로일 때만).

### Q14-1. 톤·성우 (객관식, 카테고리에 맞게)
| 톤 | 추천 보이스(예) |
|---|---|
| 터프·중저음(에너지) | Adam(Dominant), Brian(Deep), Callum(Husky) |
| 차분·다큐(안심) | Brian(Comforting), Eric(Smooth), Roger(Laid-Back) |
- `voice_settings`로 톤 미세조정: 차분/다큐 = **stability↑(0.6)·style↓(0.25)**, 강렬 = stability↓(0.4)·style↑(0.4).

### 카피 작성 원칙
- **스토리보드 막 구조에 맞춰** 6줄 내외(30초 = 천천히 ~45~60단어). 각 줄을 **막의 시작 컷**에 매핑(타임코드).
- 3안을 **서로 다른 톤/성우**로 제안해 비교하게 한다.

### 실행 (`system_v2/_gen_*_vo.py`)
```python
# POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
# headers: xi-api-key, Accept: audio/mpeg
# body: {"text":..., "model_id":"eleven_multilingual_v2", "voice_settings":{...}}
```
> **시행착오 #19:** 영상 4종 + 음악 3종처럼 **시안은 변수를 하나만 바꿔** 비교 가능하게(3 스크립트 × 1톤, 또는 1 스크립트 × 3성우). 두 변수를 동시에 흔들면 비교가 안 된다.

**산출물:** `audio/vo/{name}_{voice}.mp3` 3안.

---

## GATE 15 — 로고 (투명 PNG)

**왜:** 엔딩·자막 합성용 깔끔한 로고.

### 절차 (루마키 우회)
1. **퓨어 블랙 배경**으로 생성: Higgsfield MCP (`nano_banana_2` 또는 `gpt_image_2`), "정확한 워드마크 철자 'A E T H E R', 미니멀·프리미엄, 순흑 배경, 제품/잡요소 없음". 변형 3~4종.
   - 생성 플로우: `generate_image({model:"nano_banana_2", prompt:..., resolution:"2k"})` — medias ref 없이 순수 텍스트 생성.
2. **루마키 투명화**(Pillow): 밝기(max(r,g,b))를 알파로 → 검정은 투명, 글로우 가장자리는 자연 페이드. 그 후 **non-transparent 바운딩박스로 오토크롭**. (대안: Magnific `images_remove_background`로 알파 누끼 — 단 글로우 페이드가 필요하면 루마키가 더 자연스럽다.)
3. **제품 워드마크를 가로로**: 제품 목업을 `medias:[{role:'image', value:product_media_id}]`로 주고 "캔의 워드마크만 가로로(left-to-right) 평면 로고로, 동일 폰트·색, 순흑 배경" → 루마키.

> **시행착오 #20:** 이미지 생성 모델은 짧은 단어라도 **철자를 틀릴 수 있다** → 글자를 하나하나 명시("정확히 'AETHER', A E T H E R")로 못박고, 결과는 사람이 철자 검수. 특정 변형이 `fetch failed`로 반복 실패하면 그 변형만 보류(나머지로 충분).

**산출물:** `images/logo/*_transparent.png` (원본 블랙 + 투명 페어).

---

## GATE 16 — 최종 완성 스토리보드 조립

**왜:** 클라이언트/팀에 보여줄 **완성형 한 장 HTML**. 기획안 + 내레이션 + 컷이 한 문서에.

### 포함 요소 (`system_v2/_build_final_storyboards.py` — **번들 포함**, HALO 예시 템플릿이라 새 프로젝트는 경로·컷 교체 필요)
1. **헤더**: 프로젝트·컨셉 태그라인.
2. **기획안 개요 패널**: 컨셉·레퍼런스·타깃/톤·막 구조·컬러 서사·촬영 문법·일관성·제품 역할·기술 스펙(카드 그리드).
3. **내레이션(영문 VO·30초)**: 타임코드별 대사 + 3안/성우 안내.
4. **30컷 그리드**: 컷마다 썸네일 + **막 배지** + **타임코드(00:0X)** + 앵글/샷 + 장면 + 해당 구간 VO 라인.
- 이미지는 **최종 버전 폴더**를 소스로. 경로는 상수로 분리해 버전만 갈아끼운다.
- **base64 임베드**로 자체완결. 원본 HTML은 보존하고 `_FINAL` 새 파일로 저장(덮어쓰기 금지).
- BGM 트랙(A1)은 **외부 BGM 파일이 있을 경우 조건부**로 언급. VO(A2)는 유지.

**산출물:** `storyboard_{NAME}_FINAL_v{날짜}.html`.

---

## GATE 17 — 인터랙티브 리뷰·수정 콘솔 (자동 팝업 + 인라인 수정) ★신규

**왜:** 컷을 채팅으로 "9번 다시" 일일이 말하지 말고, **결과 HTML에서 직접 [컷 선택 → 수정요청 입력 → Enter]** 하면 그 자리에서 재생성되게 한다.

> **상태: 선택·고급 기능 — 콘솔 패키지가 `review_console/`(키트 루트)에 포함되어 있다.** 핵심 파이프라인(G1~G16)은 콘솔 없이도 작동한다. 콘솔을 쓰려면 `review_console/`에서 `python start.py --media-dir <프로젝트 이미지/영상 폴더> --mode image|video --backend agent` (원클릭: 빌드+서버+워처+브라우저). 사용법은 `review_console/START_HERE.md`, 내부 구조는 아래 스펙 참조.

### 17-0. 동작 요약 (사용자 입장)
1. 이미지를 다 뽑으면 **리뷰 콘솔 HTML이 자동으로 팝업**(브라우저)된다.
2. 맘에 안 드는 컷을 **클릭해 선택** → 그 컷 번호 칸에 **수정 요청을 한글로 입력** → **Enter**.
3. 입력 즉시 **생성 엔진(Higgsfield CLI/MCP 또는 Magnific)이 그 컷만 재생성**(이미지=nano_banana_2/gpt_image_2 또는 Magnific `images_generate`, 영상=seedance_2_0 또는 Magnific `video_generate`). 카드는 '처리중 → 완료(새 썸네일)'로 자동 갱신.
4. **모델·화질**(이미지) / **초수·화질**(영상)을 **매 수정마다 카드에서 선택**.
5. 콘솔 상단의 **"전체 영상으로 돌리기"** 버튼으로 확정 스토리보드를 **한 번에 영상화** → 끝나면 **영상 미리보기 콘솔**이 같은 디자인으로 팝업.

### 17-1. 구조 — 왜 '브리지'가 필요한가
브라우저로 연 `file://` HTML은 보안 샌드박스라 **직접 MCP를 못 부르고 파일도 못 쓴다.** → **로컬 서버 + 큐 파일 + 에이전트 워처** 3단 브리지로 잇는다.

> 아래 다이어그램·코드 스케치는 **개념 설명**이다. 실제 구현은 `review_console/` 패키지에 들어 있고(`start.py`·`build_console.py`·`review_server.py`·`worker.py`) — 본문의 `system_v2/...` 경로 표기는 설계 당시 것이니, 실행은 17-2의 `start.py` 한 줄로 하면 된다.
```
[브라우저: 리뷰 콘솔 HTML]
   │ (1) 카드 선택 → 수정요청 입력 → Enter
   │     fetch POST /revise  {type, cut, request, model, quality, duration}
   ▼
[로컬 서버  system_v2/review_server.py  (예: http://localhost:8765)]
   │ (2) revision_queue.jsonl 에 한 줄 append, 즉시 200 반환 (HTML은 '처리중' 표시)
   ▼
[에이전트 워처  (백그라운드 Agent 위임)]
   │ (3) 큐 폴링 → 항목별 처리 (동시 8 한도 준수)
   │     · 이미지: media_upload(원본 컷) → generate_image(model, prompt=수정요청, medias:[{role:'image',value:media_id}], resolution=화질)
   │     · 영상  : media_upload(원본 컷) → generate_video(seedance_2_0, prompt=수정요청, duration=초수, resolution=화질, medias:[{role:'start_image',value:media_id}])
   │ (4) 결과를 새 버전 폴더에 저장 → results.json 갱신
   ▼
[HTML] (5) results.json 을 4초마다 폴링 → 해당 카드 썸네일·상태칩 자동 교체
```

### 17-2. 자동 팝업 (에이전트가 생성 직후 실행)
```
# review_console/ 패키지가 전부 자동 처리 — 한 줄이면 된다:
python review_console/start.py --media-dir <프로젝트 이미지/영상 폴더> --mode image|video --backend agent --title "리뷰"
#   → 콘솔 HTML 빌드 + 로컬 서버 + 브라우저 오픈 + 큐 워처를 한 번에.
# --backend agent: 워커는 큐만 쌓고, Claude 에이전트가 Higgsfield MCP로 실제 재생성.
# (기본값 --backend mock 은 데모 전용 — 실제 생성 안 됨. 반드시 --backend agent 사용.)
# 사용자가 "리뷰 큐 처리해줘" 하면 에이전트가 runtime/revision_queue.jsonl 을 읽어 처리.
```

### 17-3. A. 이미지 리뷰 콘솔 (UI 설계)
- **레이아웃**: 헤더+카드 그리드, `#0b0d12` 다크, 16:9 썸네일.
- **카드 구성**:
  - 썸네일 + 컷번호 배지(C09) + 막(Act) 배지
  - **클릭 → 선택 토글**(하이라이트, 다중 선택 가능)
  - 선택 시 펼쳐지는 **수정 패널**:
    | 컨트롤 | 옵션 |
    |---|---|
    | 모델 (드롭다운) | Higgsfield **`nano_banana_2`(기본)**/`gpt_image_2` · Magnific `images_generate` |
    | 화질 (드롭다운) | 1k / **2k** / 4k |
    | 수정 요청 (입력창) | 한글 자유 입력, **Enter=제출**(Shift+Enter=줄바꿈) |
    | 상태칩 | 대기 → 처리중 → 완료 |
- **상단바**: 기본 모델·화질 셀렉트, **[선택 컷 일괄 수정]**, **[전체 영상으로 돌리기]** 버튼.

### 17-4. B. 영상 리뷰 콘솔 (UI 설계)
- 이미지 콘솔과 **동일 디자인**, 카드만 `<video autoplay muted loop playsinline>` 미리보기.
- **수정 패널**:
  | 컨트롤 | 옵션 |
  |---|---|
  | 초수 (드롭다운) | **4** / 6 / 8s |
  | 화질 (드롭다운) | 480p / 720p / **1080p** |
  | 수정 요청 (입력창) | 한글 자유 입력, **Enter=제출** → Seedance 2.0 재생성 |
  | 상태칩 | 대기 → 처리중 → 완료 |
- **상단바**: **[전체 스토리보드 → 영상 일괄 생성]**(배치, 동시 8 큐), 기본 초수·화질.

### 17-5. 핵심 코드 스케치

**(1) 로컬 서버 `system_v2/review_server.py`**
```python
import http.server, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 번들 루트 자동 탐지(절대경로 하드코딩 금지)
PORT = 8765
SERVE_DIR = os.environ["REVIEW_DIR"]
QUEUE = os.path.join(ROOT, "system_v2", "revision_queue.jsonl")
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k): super().__init__(*a, directory=SERVE_DIR, **k)
    def do_POST(self):
        if self.path == "/revise":
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            with open(QUEUE,"a",encoding="utf-8") as f: f.write(json.dumps(body,ensure_ascii=False)+"\n")
            self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(b'{"ok":true}')
        else: self.send_error(404)
http.server.ThreadingHTTPServer(("127.0.0.1",PORT), H).serve_forever()
```

**(2) HTML 인터랙션 (카드별, Enter 제출 + 폴링)**
```javascript
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault();
    fetch('/revise', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ type:'image', cut: card.dataset.cut, request: input.value,
        model: card.querySelector('.model').value, quality: card.querySelector('.quality').value })})
      .then(()=> setChip(card,'처리중'));
  }});
// 4초마다 results.json 폴링 → 완료된 컷 썸네일/상태 교체 (캐시버스터 ?t=Date.now())
```

**(3) 에이전트 워처 (백그라운드 Agent에 위임 — 동시 8 준수)**
```
revision_queue.jsonl 의 새 줄을 읽어 항목별로:
  이미지 → media_upload(원본 PNG) → generate_image({model, prompt:request, resolution:quality,
            medias:[{role:'image', value:media_id}]}) → 새 버전 폴더 저장
  영상   → media_upload(원본 컷) → generate_video({model:'seedance_2_0', prompt:request,
            duration, resolution:quality, medias:[{role:'start_image', value:media_id}]}) → 저장
  결과 경로를 results.json[cut] 에 기록(HTML이 폴링해 갱신).
처리 실패(fetch failed/preset/NSFW)는 GATE 12의 핸들링 그대로 재시도.
```

### 17-6. 수정 = 새 버전 (절대 규칙 유지)
모든 재생성은 **새 버전 폴더**(`v..._v{n+1}`)에 저장하고 원본 보존(GATE 11). `results.json`이 "현재 보여줄 최신 버전"을 가리키게 해 콘솔이 항상 최신을 띄운다.

### 17-7. 패키지 구성 (`review_console/` — 번들에 포함)
- `start.py` — 원클릭(빌드+서버+워처+브라우저). **실행 진입점.**
- `build_console.py` — `--mode image|video`로 리뷰 콘솔 HTML 빌드.
- `review_server.py` — 로컬 서버(`/revise` 큐 인입, `/` 정적 서빙).
- `worker.py` — 큐 워처 / `webroot/` — 콘솔 UI / `requirements.txt` — Pillow 등.
- 런타임 파일(자동 생성): `runtime/revision_queue.jsonl`(요청 큐), `runtime/results.json`(상태·최신경로) — `review_console/runtime/` 폴더에 위치.

> **주의:** Higgsfield 이미지 모델(`nano_banana_2`/`gpt_image_2`)의 정확한 파라미터(resolution 라벨·medias role)는 호출 전 `models_explore(action='get', model_id=...)`로 확정한다. 영상은 `seedance_2_0`. 동시 8 한도·폴링 위임은 GATE 12와 동일.
