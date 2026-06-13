# Background Run Pattern

Long-running jobs should be dispatched in the background immediately, so the main conversation continues without blocking.

## When to Background

Dispatch in the background when the job takes more than ~10 seconds and the result is not needed before the next step:

| Category | Examples |
|----------|---------|
| Video generation | Any video model call (Seedance, Kling, Veo, Sora, Runway, Higgsfield) |
| Slow image generation | High-quality or batch image jobs (2+ images at once) |
| Audio / BGM | Music generation (Suno), long TTS (ElevenLabs) |
| Post-processing | ffmpeg assembly, upscaling, beat analysis |

## Rules

- Dispatch the background job **first**, before doing anything else
- Immediately after dispatching, report one line: `"Background started — {job} / ~{eta}"`
- Continue with other work or respond to the user — do not wait or poll
- When the completion notification arrives, summarize the result and suggest the next step
- Do not fake completion — only report done when the notification comes back

## Pattern

```
1. User requests a long-running job
2. Dispatch with run_in_background: true
3. One-line status: "Background started — video generation / ~2 min"
4. Continue conversation
5. [Notification arrives] → summarize result → suggest next step
```
