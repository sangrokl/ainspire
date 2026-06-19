# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workspace Purpose

This is a personal AI learning and tooling workspace. It is not a software product — it is a collection of Claude Code setup packages, video production tools, and output artefacts.

## Folder Structure

```
00. AInspire/          ← Installable Claude Code setup packages (see below)
01. ABOUT ME/          ← (empty — personal reference)
02. OUTPUTS/           ← Deliverable files, in YYYYMMDD_ProjectName/ subfolders
03. TEMPLATES/         ← Reusable scripts/tools, in YYYYMMDD_ProjectName/ subfolders
04. ASSETS/            ← Source materials staged by the user for a task — read from here first
99. 자료실/            ← Read-only reference library: AInspire course PDFs, videos, package sources
```

### Saving Files

- Deliverables → `02. OUTPUTS/YYYYMMDD_ProjectName/`
- Reusable scripts/tools → `03. TEMPLATES/YYYYMMDD_ProjectName/`
- Never save loose files directly in the OUTPUTS or TEMPLATES roots.

## AInspire Packages (`00. AInspire/`)

Each subfolder is a self-contained install package. When the user says "설치.md 읽고 세팅해줘", read `설치.md` inside that folder and execute it directly.

| Package | What it installs |
|---------|-----------------|
| `0.1 claude-basic-setup` | Global `~/.claude/CLAUDE.md` rules + `settings.json` permissions + `agent-team`, `background-run` skills |
| `0.2 claude-video-setup` | `seedance-prompt` skill |
| `0.3 claude-writing-helper` | `humanizer`, `translator` skills |
| `0.4 claude-premiere-mcp` | Adobe Premiere Pro MCP server (Node.js/TypeScript) |

## Premiere MCP Server (`00. AInspire/0.4 claude-premiere-mcp/`)

Before doing any work in this subfolder, read its own `CLAUDE.md` — it has the full Korean-language setup workflow, including environment checks Claude must perform before touching anything.

Requires Node 18+, Premiere Pro 2020+.

```bash
# Build
npm install && npm run build        # produces dist/index.js

# Full macOS install (deps + build + CEP panel copy + debug mode + Claude Desktop config)
npm run setup:mac

# Diagnose a broken setup
npm run setup:doctor:mac            # or :win on Windows

# Uninstall
npm run uninstall:mac               # or :win on Windows

# Register with Claude Code (after build)
claude mcp add premiere-pro -s user -e PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge -- node /absolute/path/to/dist/index.js

# Dev (lint / test / format)
npm run lint && npm test && npm run format
```

After install, inside Premiere: Window → Extensions → MCP Bridge (CEP) → set Temp Dir → Save → Start Bridge → Test Connection.

Common failure: tools fail even though the MCP server is listed → Premiere is not open, no project is loaded, or the CEP panel has not been started.

### Premiere MCP Internal Architecture

The `설치.md` in `0.4` supports multiple AI clients (Claude Code, Claude Desktop, Codex, Cursor, etc.) — not just Claude Code. The setup script only registers Claude Desktop; other clients must be registered manually per the `설치.md` step 3.

The server communicates with Premiere via a **file-based IPC** through a shared temp directory (`PREMIERE_TEMP_DIR`). Understanding this is essential for debugging:

| Layer | Path | Role |
|-------|------|------|
| Entry point | `src/index.ts` | Instantiates and wires all modules; runs as stdio MCP server |
| Bridge | `src/bridge/index.ts` | Writes ExtendScript command files to temp dir; polls for result files; handles UXP transport |
| Tools | `src/tools/index.ts` | MCP tool definitions (what the AI can call) |
| Resources | `src/resources/index.ts` | MCP resource definitions (read-only data the AI can access) |
| Prompts | `src/prompts/index.ts` | Reusable MCP prompt templates |
| CEP panel | `cep-plugin/` | Runs inside Premiere; polls the temp dir and executes ExtendScript |
| UXP plugin | `uxp-plugin/` | Alternative transport (UXP API instead of CEP) |

The bridge module embeds ExtendScript helpers directly as a string and writes them to temp files for Premiere to pick up. If tools time out, the problem is almost always in the CEP panel side (not started, wrong temp dir, or Premiere crashed).

## Video Pipeline Tools (`03. TEMPLATES/VideoTools/`)

Reusable tool — undated, unlike other `03. TEMPLATES/` subfolders.

`video_pipeline.py` — YouTube URL → 9:16 crop → Whisper subtitles → burned-in MP4.

```bash
python3 video_pipeline.py "<YouTube URL>" <start_sec> <end_sec> [output_name]
```

Outputs land in `02. OUTPUTS/YYYYMMDD_<output_name>/` automatically.

`subtitle_burner.py` — standalone SRT burn-in tool.

```bash
python3 subtitle_burner.py input.mp4 subtitles.srt output.mp4
```

Both scripts require: `Pillow`, `yt-dlp`, `ffmpeg`, `openai-whisper`.

To change Whisper model or language, edit the constants at the top of `video_pipeline.py` (`WHISPER_MODEL`, `WHISPER_LANGUAGE`).

## Contest Production Template (`03. TEMPLATES/20260613_공모전 제작/`)

This subfolder holds the working context for competition/contest video production sessions. It has a `.claude/` project-settings directory. The established workflow for this template:

1. Generate a character sheet first (establish visual consistency before any scene work)
2. Use Opus for planning/creative direction tasks
3. Reference the character sheet in every generation prompt to maintain consistency across scenes

## 99. 자료실

Read-only reference material — do not modify. Contains:

- `01. 패키지 자료/` — source archives for the AInspire packages
- `02–05. N기 자료/` — weekly course PDFs and videos for AInspire cohorts (2기–4기)
- `70. marketingskills/` — source copy of the marketing-skills Claude Code plugin (v2.4.1); the installed version used by this workspace lives here

The marketing-skills plugin (`70. marketingskills/`) provides 40+ marketing skills invoked via `/marketing-skills:<skill-name>` and 51 zero-dependency Node.js CLI tools in `tools/clis/`.

```bash
# Validate skill YAML frontmatter
bash 99.\ 자료실/70.\ marketingskills/validate-skills.sh

# Run a CLI tool
node 99.\ 자료실/70.\ marketingskills/tools/clis/<name>.js
```
