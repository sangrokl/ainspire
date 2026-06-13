# Adobe Premiere Pro MCP

이 폴더는 AI 에이전트가 Adobe Premiere Pro를 자연어로 조작할 수 있게 해주는 MCP 서버다.
사용자가 이 폴더에서 설치·셋업 의도를 보이면 **`설치.md`를 읽고 그대로 진행한다.**
(Claude Code, Codex, Cursor 등 어떤 에이전트든 절차는 동일하다.)

## 핵심 요약

이 도구는 폴더만 있다고 작동하지 않는다. 다음이 모두 갖춰져야 한다:

1. Node.js 18+ 로 빌드 (`npm install` + `npm run build` → `dist/index.js`)
2. Adobe CEP 확장 복사 (Windows: `%APPDATA%\Adobe\CEP\extensions\MCPBridgeCEP`,
   macOS: `~/Library/Application Support/Adobe/CEP/extensions/MCPBridgeCEP`)
3. CEP debug mode 활성화 (Windows: `HKCU:\Software\Adobe\CSXS.*` → `PlayerDebugMode=1`,
   macOS: `defaults write com.adobe.CSXS.* PlayerDebugMode 1`)
4. **지금 사용 중인 클라이언트에 MCP 등록** — setup 스크립트는 Claude Desktop에만
   등록하므로, Claude Code / Codex / 기타 클라이언트는 별도 등록이 필요하다.
   명령은 `설치.md` 3단계 참고.
5. 프리미어에서 패널 시작 (창 → 확장 → MCP Bridge (CEP) → Start Bridge)

1~3은 `npm run setup:win`(Windows) / `npm run setup:mac`(macOS) 스크립트가 자동 수행한다.
한 줄씩 직접 재현하지 말고 스크립트를 신뢰하고 그대로 쓴다.

## 진행 원칙

- 설치 전에 현재 상태를 먼저 점검하고(Node 버전, 빌드 여부, CEP 복사 여부,
  debug mode, 클라이언트 등록 여부), 빠진 항목만 정리해서 사용자에게
  "자동으로 설치해드릴까요?" 한 번에 묻는다. 동의하면 진행한다.
- Node.js, Premiere Pro 같은 외부 앱은 자동 설치 불가 — 다운로드 링크만 안내한다.
- 설치 후 직접 검증한다: `dist/index.js` 존재, `MCPBridgeCEP` 복사됨,
  자기 클라이언트에 `premiere-pro` 항목 등록됨.
- 문제가 생기면 `npm run setup:doctor:win` / `setup:doctor:mac`으로 진단한다.
- 사용자가 설치 얘기를 꺼내지 않았는데 마음대로 점검·설치를 시작하지 않는다.
