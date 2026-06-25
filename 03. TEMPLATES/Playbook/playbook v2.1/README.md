# 🎞️ Portable Storyboard Kit v2 — 광고 스토리보드 제작 묶음 (Higgsfield CLI/MCP · Magnific)

광고 영상 한 편을 **기획 → 스토리보드 → 영상화 → 내레이션 → 로고 → 최종 조립**까지 만드는 휴대용 묶음.
다른 컴퓨터에서도 그대로 동작하도록 **모든 경로는 상대경로**이고, 스크립트의 `ROOT`는 파일 위치에서 자동 탐지된다.

> 🖼️ 이미지·영상 생성은 **Higgsfield(CLI 또는 MCP) / Magnific MCP**로,
> 🎙️ 내레이션은 **ElevenLabs MCP(`text_to_speech`)**로 한다(이 환경에 연결되어 있으면 별도 키 불필요; 백업1 Higgsfield TTS, 백업2 ElevenLabs 직접 API). 🎵 BGM은 **Suno 프롬프트를 제안받아 사용자가 직접 생성**(GATE 13, 키 불필요).

## 📁 폴더 구조
```
playbook v2.1/                                ← 이 폴더째 공유. 여기서 에이전트를 연다.
  CLAUDE.md / AGENTS.md                        ← 진입 규칙(폴더 열면 자동 로드). 사람도 여기부터.
  18_commercial_storyboard_playbook_v2/        ← 플레이북 5문서
    00_core.md          (항상 먼저)
    01_planning_G1-G11.md · 02_production_G12-G17.md
    03_reference_enhance-prompts.md · 04_reference_lessons-appendix.md
  system_v2/                                   ← 후처리·유틸 스크립트 + .env (ElevenLabs 직접 API 백업 경로용 키 — MCP 연결 시 불필요)
  review_console/                              ← GATE 17 리뷰 콘솔(선택) — start.py 원클릭
```

## 🆕 새 컴퓨터 준비
1. ☑️ **Node.js 18+** — `.mjs`용(전역 `fetch` 사용, 외부 npm 0개).
2. ☑️ **Python 3.9+ + Pillow** (`pip install Pillow`) — 스토리보드 HTML 빌드·로고 투명화.
3. ☑️ **ffmpeg** — 영상 조립(`assemble_video.mjs`)용.
4. 🔌 **생성 엔진 연결** (전부 OAuth, API 키 불필요 — 셋 중 최소 하나면 됨):
   - **Higgsfield MCP** *(기본 — 이것만으로 전 과정 가능)* — 데스크톱 앱 로그인. 확인 `balance`.
   - **Higgsfield CLI** *(선택 — 대량·일괄에 편함)* — ① `npm install -g @higgsfield/cli` ② `higgsfield auth login`(브라우저 5초) ③ (선택) `npx skills add higgsfield-ai/skills`(에이전트 연동 → "Higgsfield로 이미지 만들어줘"). 확인 `higgsfield account status`.
   - **Magnific MCP** *(선택 — 업스케일·누끼·Soul 학습)* — 클라이언트 MCP 설정에 `https://mcp.magnific.com` 추가 후 OAuth. 확인 `account_balance`.
5. 🎙️ **내레이션** — ElevenLabs MCP(`text_to_speech`) 연결만 있으면 OK, 별도 키·`.env` 불필요로 바로 생성.
   *(백업1: Higgsfield 연결(위 4번)만 있으면 OK — CLI `higgsfield generate create inworld_text_to_speech --prompt "..."` 또는 MCP `generate_audio`로 생성.
   백업2: ElevenLabs 직접 API 쓰려면 `system_v2/.env`를 열어 `ELEVENLABS_API_KEY` 입력(파일은 이미 있음), `node check_api_connections.mjs`로 확인.)*
   ```
   # system_v2 폴더에서 (ElevenLabs 직접 API 백업 경로 쓸 때만)
   notepad .env                  # .env 열어 ELEVENLABS_API_KEY 입력 (mac/linux: nano .env)
   node check_api_connections.mjs
   ```

## 🚀 시작하는 법
- 🤖 **에이전트(Claude Code 등)로 이 폴더를 열면** `CLAUDE.md`/`AGENTS.md`가 자동 로드되어
  에이전트가 `00_core.md`부터 단계적으로 따라간다. 그냥 "AETHER 에너지드링크 광고 만들어줘"처럼 요청하면 된다.
- 👤 사람이 읽을 땐 `18_commercial_storyboard_playbook_v2/00_core.md`부터.

## 🧰 system_v2 파일
| 용도 | 파일 |
|---|---|
| 스토리보드 HTML(base64 임베드) | `_build_halo_v5_embed.py` *(HALO 예시 템플릿)* |
| 스토리보드 HTML(base64 임베드) | `_build_RISE_embed.py` · `_build_RISE_v2_embed.py` *(RISE 예시 템플릿)* |
| 최종 완성 스토리보드 HTML | `_build_final_storyboards.py` *(HALO/AETHER 예시 템플릿)* |
| 내레이션 TTS(ElevenLabs 직접 API, 백업2 경로) | `_gen_halo_vo.py` *(템플릿 — 기본은 ElevenLabs MCP 사용, 이 스크립트는 MCP 연결이 없을 때 직접 API 백업으로만)* |
| 로고 루마키 투명화 | `_logo_transparent.py` *(템플릿)* |
| 영상 조립(ffmpeg) | `assemble_video.mjs` |
| 대시보드 매니페스트 | `generate_manifest.mjs` |
| 키 연결 확인 | `check_api_connections.mjs` |
| 공통 라이브러리 | `lib/{env,io,log}.mjs` |

> ⚠️ **이미지·영상 생성은 system_v2 스크립트가 아니라 생성 엔진**(Higgsfield CLI/MCP · Magnific)으로 한다 — `00_core.md`의 [생성 엔진] 참조.
> 이 묶음의 스크립트는 후처리·유틸·내레이션용이다.

## ⚠️ *(템플릿)* 파일 주의
`_build_halo_v5_embed.py` · `_build_final_storyboards.py` · `_gen_halo_vo.py` · `_logo_transparent.py`는 HALO/AETHER 광고 예시가 든 **작업 템플릿**이다.
내부의 `projects\halo_watch\...` 경로 · `JOBS` · `voice_id` · 파일명은 **예시값**이라
새 컴퓨터엔 그 파일이 아직 없다 → 자기 프로젝트 값으로 교체해야 동작한다. **`ROOT`만은 자동 탐지라 손댈 필요 없다.**

## 🧭 경로 portable 메모
- ✅ **절대경로(`F:\` 등) 없음.** 산출물은 전부 `이폴더/projects/{project}/{version}/...`에 상대로 쌓인다. (type 층 없음 — 프로젝트명 바로 아래 버전 폴더.)
- 묶음 폴더 이름에 공백이 있어도(예: `playbook v2`) 내부 참조는 공백 없는 상대경로라 무방.
  단 셸에서 폴더 절대경로를 직접 칠 땐 따옴표로 감쌀 것.

## 🔒 보안
- `.env`는 **빈 채로 포함**(키만 채우면 됨). ⚠️ **배포본의 `.env`엔 절대 실제 키를 넣지 말 것** — 키는 받는 사람이 입력. `.gitignore`가 `.env`·로그·`__pycache__` 커밋 차단.
- 공유/배포 전 `.env`가 **비어 있는지(키 없음)** 재확인.
