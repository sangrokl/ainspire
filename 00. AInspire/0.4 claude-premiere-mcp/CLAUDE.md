# Adobe Premiere Pro MCP

이 폴더는 Claude가 Adobe Premiere Pro를 자연어로 조작할 수 있게 해주는 MCP 서버다.
사용자가 이 폴더에서 무언가를 시도하면, 가장 먼저 환경이 제대로 갖춰져 있는지를
확인하고 빠진 게 있으면 사용자를 도와 설치를 끝내준다.

## 사용자가 이 폴더에 처음 들어왔다면

아마도 MCP를 쓰려고 온 것이다. 그런데 이 도구는 단순히 폴더만 있다고 작동하지
않는다. Node.js로 빌드해야 하고, Adobe CEP 확장도 시스템 폴더로 복사돼야 하며,
사용 중인 MCP 클라이언트(Claude Desktop, Claude Code 등)에도 서버 등록이 필요하다.

그러니 사용자가 "쓰고 싶다", "켜고 싶다", "설치", "셋업" 같은 의도를 보이면,
먼저 지금 상태를 직접 점검해본다. Node.js 버전, Premiere Pro 설치 여부,
node_modules·dist 빌드 상태, CEP 확장 복사 여부, CEP debug mode
활성화 여부, 클라이언트의 premiere-pro 항목 등록 여부(Claude Desktop이면
claude_desktop_config.json, Claude Code면 `claude mcp list`) — 이런 것들을
조용히 확인해서 정리한다.

OS에 따라 경로가 다르다. Windows면 `%APPDATA%\Adobe\CEP\extensions`,
`%APPDATA%\Claude\claude_desktop_config.json`, 레지스트리 `HKCU:\Software\Adobe\CSXS.*`
쪽을 보고, macOS면 `~/Library/Application Support/Adobe/CEP/extensions`,
`~/Library/Application Support/Claude/claude_desktop_config.json`,
`defaults read com.adobe.CSXS.*`로 본다. Linux는 Premiere가 없으니 거기서
설명만 해주고 끝낸다.

## 빠진 게 있으면 사용자에게 도와줘도 되냐고 묻기

점검 결과를 보여주고 빠진 항목만 정리해서 "이거 자동으로 설치해드릴까요?"
한 번에 묻는다. 사용자가 동의하면 진행한다.

다만 Node.js, Adobe Premiere Pro, Claude Desktop 같은 외부 앱은 자동으로
못 깔아준다. 이건 사용자가 직접 받아야 하므로 다운로드 링크만 알려준다.
(Node.js는 nodejs.org LTS, Premiere는 Adobe Creative Cloud, Claude Desktop은
claude.ai/download.) 사용자가 설치 마쳤다고 하면 점검부터 다시 시작한다.

## 실제 설치는 setup 스크립트가 다 한다

내부 셋업(의존성 설치, 빌드, CEP 복사, debug mode, Claude Desktop config 등록 등)은
이미 잘 작성된 스크립트가 있다. Windows면 `npm run setup:win`, macOS면
`npm run setup:mac`을 호출하면 된다. 한 줄씩 직접 재현하지 말고 이 스크립트를
신뢰하고 그대로 쓴다.

단, 스크립트는 MCP를 **Claude Desktop에만** 등록한다. 지금 Claude Code에서
실행 중이라면 추가로 등록해야 한다 (자세한 치환 규칙은 `설치.md` 3단계):

```
claude mcp add premiere-pro -s user -e PREMIERE_TEMP_DIR=<TEMP경로> -- node <폴더경로>/dist/index.js
```

스크립트가 끝나면 직접 확인한다 — dist/index.js가 만들어졌는지, CEP extensions
폴더에 MCPBridgeCEP가 복사됐는지, 자기 클라이언트에 premiere-pro
항목이 들어갔는지. 셋 다 OK면 사용자에게 마지막 안내를 해준다: 클라이언트와
Premiere를 재시작하고, Premiere의 Window → Extensions → MCP Bridge (CEP)를 열어
Temp Directory를 설정하고 Save → Start Bridge → Test Connection까지 누르면
연결된다.

중간에 뭔가 실패하면 `npm run setup:doctor:win` 또는 `npm run setup:doctor:mac`을
돌려서 어디서 막혔는지 진단한다.

## 톤

사용자가 따로 설치 얘기를 꺼내지 않았는데 마음대로 점검·설치를 시작하지 않는다.
필요한 시점이 됐을 때만, 그리고 진행 전에는 반드시 한 번 확인을 받는다.
시스템에 손대는 작업이라는 점을 잊지 않는다.
