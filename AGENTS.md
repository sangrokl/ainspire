# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Workspace Purpose

This is a personal AI learning and tooling workspace. It is not a software product — it is a collection of Codex setup packages, video production tools, and output artefacts.

## Folder Structure

```
00. AInspire/          ← Installable Codex setup packages
01. ABOUT ME/          ← (empty — personal reference)
02. OUTPUTS/           ← Deliverable files (videos, HTML, etc.), date-prefixed subfolders
03. TEMPLATES/         ← Reusable scripts and tools, date-prefixed subfolders
04. ASSETS/            ← Source materials staged by the user for a task — read from here first
```

### Saving Files

- Deliverables → `02. OUTPUTS/YYYYMMDD_ProjectName/`
- Reusable scripts/tools → `03. TEMPLATES/YYYYMMDD_ProjectName/`
- Never save loose files directly in OUTPUTS or TEMPLATES roots

## AInspire Packages (`00. AInspire/`)

Each subfolder is a self-contained install package. When the user says "설치.md 읽고 세팅해줘", read `설치.md` inside that folder and execute it directly.

| Package | What it installs |
|---------|-----------------|
| `0.1 Codex-basic-setup` | Global `~/.Codex/AGENTS.md` rules + `settings.json` permissions + `agent-team`, `background-run` skills |
| `0.2 Codex-video-setup` | `seedance-prompt` skill |
| `0.3 Codex-writing-helper` | `humanizer`, `translator` skills |
| `0.4 Codex-premiere-mcp` | Adobe Premiere Pro MCP server (Node.js/TypeScript) |

## Premiere MCP Server (`0.4 Codex-premiere-mcp/`)

MCP server that lets Codex control Premiere Pro via natural language. Requires Node 18+, Premiere Pro 2020+.

```bash
# Build
npm install && npm run build        # produces dist/index.js

# Full macOS install (deps + build + CEP panel copy + debug mode + Codex Desktop config)
npm run setup:mac

# Diagnose a broken setup
npm run setup:doctor:mac            # or :win on Windows

# Register with Codex (after build)
Codex mcp add premiere-pro -s user -e PREMIERE_TEMP_DIR=/tmp/premiere-mcp-bridge -- node /absolute/path/to/dist/index.js
```

After install, inside Premiere: Window → Extensions → MCP Bridge (CEP) → set Temp Dir → Save → Start Bridge → Test Connection.

Common failure: tools fail even though the MCP server is listed → Premiere is not open, no project is loaded, or the CEP panel is not started.

## Video Pipeline Tools (`03. TEMPLATES/`)

`video_pipeline.py` — YouTube URL → 9:16 crop → Whisper subtitles → burned-in MP4.

```bash
python3 video_pipeline.py "<YouTube URL>" <start_sec> <end_sec> [output_name]
```

Outputs land in `../../02. OUTPUTS/` (relative to script location) under a dated subfolder.

`subtitle_burner.py` — standalone SRT burn-in tool.

```bash
python3 subtitle_burner.py input.mp4 subtitles.srt output.mp4
```

Both scripts require: `Pillow`, `yt-dlp`, `ffmpeg`, `openai-whisper`.
