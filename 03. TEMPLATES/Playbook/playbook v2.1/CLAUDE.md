# 🎬 광고 스토리보드 파이프라인 (v2) — 에이전트 진입 규칙

이 폴더는 광고 영상 한 편을 **기획 → 스토리보드(이미지) → 영상화 → 내레이션 → 로고 → 최종 조립**까지
객관식 인터뷰로 만드는 **플레이북 묶음**이다. 이 파일은 자동으로 읽히는 진입점이다.

## 🔌 STEP 0 — 생성 엔진 연결 확인 (다른 무엇보다 먼저)
이미지·영상 생성은 생성 엔진(Higgsfield CLI/MCP 또는 Magnific MCP)으로 한다. **작업을 시작하면 제일 먼저 연결을 확인하고, 안 되어 있으면 연결부터 끝낸 뒤 진행한다. 셋 중 최소 하나면 된다.**
1. ✅ **확인:** Higgsfield CLI `higgsfield account status` → 정상이면 CLI 기본 사용. CLI 없으면 Higgsfield MCP `balance` / Magnific `account_balance` 순으로 확인.
2. 🔑 **인증만 안 됨:** CLI `higgsfield auth login`(브라우저 OAuth) / Higgsfield MCP `authenticate`→로그인→`complete_authentication` / Magnific 첫 호출 시 브라우저 OAuth.
3. 📦 **설치/서버 자체가 없음:**
   - **Higgsfield CLI (기본):** 미설치면 사용자에게 안내 — `npm install -g @higgsfield/cli` → `higgsfield auth login` → (선택) `npx skills add higgsfield-ai/skills`.
   - Higgsfield MCP (백업): 데스크톱 앱 로그인 후 클라이언트에 연결 (사용자 요청).
   - Magnific MCP: 클라이언트 MCP 설정에 `https://mcp.magnific.com`(streamable HTTP) 추가 → OAuth (사용자 요청).
4. 🟢 **CLI가 연결되면 CLI로 진행(G8 이후) — CLI 없을 때만 MCP로 대체.** 역할 분담: 일괄·무인=CLI, 단발 즉석=MCP, 업스케일/누끼=Magnific. **내레이션(TTS) = ElevenLabs MCP(`text_to_speech`)**(이 환경에 연결되어 있으면 별도 키 불필요) — 기본. *(백업1: Higgsfield TTS(`inworld_text_to_speech`) — CLI `higgsfield generate create inworld_text_to_speech` 또는 MCP `generate_audio`, Higgsfield 연결만 있으면 됨. 백업2: ElevenLabs 직접 API — `system_v2/.env`의 `ELEVENLABS_API_KEY`, `node system_v2/check_api_connections.mjs`로 확인.)*

## ⭐ 시작 규칙 (반드시 지켜라)
0. ✅ **위 [STEP 0]에서 생성 엔진 연결을 먼저 확인·완료한다.** (안 되어 있으면 생성 단계로 가지 말 것)
1. 📖 광고/스토리보드 제작을 시작하면 **먼저 `18_commercial_storyboard_playbook_v2/00_core.md` 하나만 읽어라.**
2. 🧭 그다음은 00_core의 **로딩 가이드**가 시키는 대로 **필요할 때 한 파일씩만** 연다:
   - 🎯 기획(G1~G11) → `18_commercial_storyboard_playbook_v2/01_planning_G1-G11.md`
   - 🎬 제작(G12~G17) → `18_commercial_storyboard_playbook_v2/02_production_G12-G17.md`
   - 💡 생성 직전(규칙0·ENHANCE 상수 풀텍스트) → `18_commercial_storyboard_playbook_v2/03_reference_enhance-prompts.md`
   - 📚 시행착오·세션로그·용어 → `18_commercial_storyboard_playbook_v2/04_reference_lessons-appendix.md`
3. 🚫 **처음에 5개 문서를 한꺼번에 통독하지 마라.** 컨텍스트 낭비이며 의도된 사용법이 아니다.

## 📁 작업 디렉터리·경로 (공유용 — 절대경로 금지)
- **이 폴더가 작업 루트다.** 여기서 실행한다. 문서는 `18_commercial_storyboard_playbook_v2/...`, 스크립트는 `system_v2/...`로 참조.
- ⚠️ 모든 경로는 **상대경로**다. `F:\`·`C:\` 같은 절대경로를 새로 만들지 마라.
- 스크립트의 `ROOT`는 파일 위치(`__file__`)에서 자동 탐지되므로 PC·드라이브가 달라도 동작한다. 산출물은 `이폴더/projects/{project}/{version}/`에 쌓인다.

**버전 폴더 표준 구조 (항상 이 구조를 만들고 유지한다):**
```
{version}/
├── assets/              ← 모든 생성 소재 (하위 폴더만 노출)
│   ├── audio/           ← TTS · VO · SFX 파일
│   ├── images/          ← 생성 이미지 컷
│   ├── videos/          ← 생성 영상 컷
│   ├── md/              ← scenario.md · tvcf_archetypes.md 등 문서
│   └── ref/             ← 참조 원본 (수정 금지)
│       ├── logo/
│       ├── product/
│       └── main_character/
├── output/              ← 최종 조립 영상 · 내보내기 파일
└── preview/             ← 스토리보드 HTML · 영상 리뷰 HTML
```
**탑레벨에 보이는 폴더: `assets/` · `output/` · `preview/` 3개만.** 낱개 파일·기타 폴더를 탑레벨에 두지 않는다.

## 🛠️ 생성 스택
- 🖼️ **이미지·영상 = Higgsfield CLI(기본) / Higgsfield MCP(백업) / Magnific MCP(업스케일 전용)** (전부 OAuth, API 키 불필요). 경로·특성은 `00_core.md`의 [생성 엔진] 표 참조.
  - **Higgsfield CLI** *(기본)*: 대량 일괄·무인에 최적(`--wait` 폴링, `--json` 배치, 결과 URL→다운로드). **이것만으로 전 과정 가능.** **미설치 시 사용자에게 안내:** `npm install -g @higgsfield/cli` → `higgsfield auth login` → (선택) `npx skills add higgsfield-ai/skills`. (상세 = `00_core.md` [CLI 설치 안내])
  - **Higgsfield MCP** *(백업)*: CLI 없을 때 사용. 데스크톱 앱 OAuth. 세션 내 즉석 단발에 편함.
  - **Magnific MCP** *(선택)*: 클라이언트 MCP 설정에 `https://mcp.magnific.com` 추가 후 OAuth. 업스케일·누끼·Soul 학습 전용.
- 🎙️ **내레이션(VO) = ElevenLabs MCP(`text_to_speech`)** — 이 환경에 연결되어 있으면 바로 사용, 별도 키 불필요. *(백업1: Higgsfield TTS(`inworld_text_to_speech`) — CLI `higgsfield generate create inworld_text_to_speech --prompt "..."` 또는 MCP `generate_audio`, Higgsfield 연결만 있으면 OK. 백업2: ElevenLabs 직접 API — `system_v2/.env`에 `ELEVENLABS_API_KEY`)*
- 🎵 **BGM = Suno 프롬프트 제안(GATE 13) → 사용자가 직접 생성** — 에이전트는 Suno 프롬프트만 제안, 실제 생성은 사용자(별도 키 불필요). 후처리(HTML·로고·조립)는 `system_v2`의 Python/ffmpeg.

## ⛔ 불변 규칙 (요약 — 풀텍스트는 00_core·03)
- 모든 이미지/영상에 **규칙0 프리픽스 + ENHANCE 상수** 주입. **영상은 No-BGM · SFX only.**
- 🚫 생성물 **덮어쓰기 금지**(새 버전 폴더). 생성 이미지를 **Read로 열지 말 것**(경로만). 실존 상표는 **디자인 언어로** 묘사.
- ✅ 생성 직전 **모델·해상도·오디오·비율 4종 + 프리뷰 승인**.
