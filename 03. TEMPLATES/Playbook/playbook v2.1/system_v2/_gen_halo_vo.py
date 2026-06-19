# -*- coding: utf-8 -*-
import os, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, r"projects\halo_watch\v2026-05-29_v10\audio\vo")
os.makedirs(OUT, exist_ok=True)

KEY = None
for line in open(os.path.join(SYS, ".env"), encoding="utf-8"):
    if line.startswith("ELEVENLABS_API_KEY="):
        KEY = line.split("=", 1)[1].strip()
assert KEY, "no ELEVENLABS_API_KEY in .env"

MODEL = "eleven_multilingual_v2"
# calm documentary delivery: steadier (higher stability), restrained (low style)
SETTINGS = {"stability": 0.60, "similarity_boost": 0.80, "style": 0.25, "use_speaker_boost": True}

# (out_name, voice_id, voice_label, text)  -- calm American male documentary voices
JOBS = [
 ("halo_vo_A_brian", "nPczCjzI2devNBz1zQrb", "Brian (Deep, Comforting)",
  "He went up alone, the way he liked it. A loose rock, a hard fall, no way down, and no signal to call for help. But his watch felt the fall. It reached for help, and told them exactly where he was. That night, the mountain didn't keep him. HALO. It watches, so someone always knows."),
 ("halo_vo_B_eric", "cjVigY5qzO86Huf0OWal", "Eric (Smooth, Trustworthy)",
  "Most days, nothing happens. That's the point. But when he fell, miles from anyone, his phone was useless. His watch wasn't. It detected the fall, called for help, and shared his location. He was found in minutes. HALO. Quietly looking out for you."),
 ("halo_vo_C_roger", "CwhRBWXzGAHq8TQ4Fs17", "Roger (Laid-Back, Resonant)",
  "We don't plan for the moment things go wrong. A fall on an empty trail. The light fading, the cold setting in. One device kept its signal, and called for help on its own. He made it home that night. HALO. Always one step ahead of the worst."),
]

ok = 0
for name, vid, label, text in JOBS:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS}).encode()
    req = urllib.request.Request(url, data=body, method="POST",
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        r = urllib.request.urlopen(req, timeout=120); data = r.read()
        open(os.path.join(OUT, name + ".mp3"), "wb").write(data)
        print(f"OK  {name}  [{label}]  {len(data)//1024} KB"); ok += 1
    except urllib.error.HTTPError as e:
        print(f"FAIL {name}  HTTP {e.code}: {e.read()[:200]}")
    except Exception as e:
        print(f"FAIL {name}  {str(e)[:200]}")
print(f"done {ok}/{len(JOBS)} -> {OUT}")
