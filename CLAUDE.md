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

# Register with Claude Code (after build)
claude mcp add premiere-pro -s user -e PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge -- node /absolute/path/to/dist/index.js
```

After install, inside Premiere: Window → Extensions → MCP Bridge (CEP) → set Temp Dir → Save → Start Bridge → Test Connection.

Common failure: tools fail even though the MCP server is listed → Premiere is not open, no project is loaded, or the CEP panel has not been started.

## Video Pipeline Tools (`03. TEMPLATES/`)

Scripts live in dated subfolders (e.g. `03. TEMPLATES/20260613_VideoTools/`). Find the most recent subfolder before running.

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

## 99. 자료실

Read-only reference material — do not modify. Contains:

- `01. 패키지 자료/` — source archives for the AInspire packages
- `02–04. N기 자료/` — weekly course PDFs and videos for AInspire cohorts (3기, 4기, etc.)
