// VOLT v20260617 — 30컷 이미지 일괄 생성 (Higgsfield CLI, nano_banana_2)
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const execFileP = promisify(execFile);
const ROOT = dirname(fileURLToPath(import.meta.url));
const IMG_DIR = join(ROOT, "images");
const REF_FACE = join(ROOT, "images/ref/ref_face_v2.png");
const REF_PRODUCT = join(ROOT, "images/ref/ref_product.png");

mkdirSync(IMG_DIR, { recursive: true });

const RULE0_IMG = `MANDATORY IMAGE PREFIX (append to EVERY image prompt, no exceptions):
— FOV & COMPOSITION: ZERO front-facing, ZERO eye-level. The subject NEVER looks into the lens. Use ONLY low-angle, high-angle or dutch-angle framing; off-center rule-of-thirds; telephoto shallow-DOF (demai) with clear 3-layer FG/MG/BG depth separation. ONE dominant face in tight CU / OTS — never a flat two-shot.
— BACKLIGHT: hard warm backlight / rim-light from behind tracing the subject's silhouette, separating it from background. Motivated key from a window/blinds. NO flat frontal fill light.
— NEGATIVE FILL: black negative fill on the shadow side — one side falls into deep controlled shadow; sculpt the form, raise contrast, kill flat ambient. LOW-KEY only, NEVER high-key, no blown highlights.`;

const IMG_ENHANCE = `CINEMATIC PHOTOREAL — REQUIRED ENHANCEMENT: heightened photoreal realism with ENHANCED FACIAL DETAIL (lifelike skin micro-texture, visible pores, subsurface scattering, sharp eye catchlights); a real frame from a premium TV commercial, never CGI/3D-render/illustration. ABSOLUTELY NO front-facing and NO eye-level framing. Aggressively use TV-CF camera grammar: LOW-ANGLE, HIGH-ANGLE, DUTCH-ANGLE; off-center rule-of-thirds; dynamic wide-angle AND shallow-depth-of-field telephoto close-ups (demai bokeh) with clear 3-layer FG/MG/BG depth. BACKLIGHT MANDATORY. NEGATIVE FILL MANDATORY. LOW-KEY luxurious grade (NEVER high-key): deep controlled shadows, restrained highlights, premium cinematic mood. Compose so each cut CONNECTS to its neighbours via match-cuts / natural transitions. Frame as a keyframe primed for dynamic video motion.`;

const GRADE = {
  AWAY: "GRADE: AWAY — cool blue dawn palette, desaturated, melancholic premium tone.",
  WARM: "GRADE: WARM — cool blue gradually bleeding into warm tungsten light, transitional premium tone.",
  HOME: "GRADE: HOME — warm tungsten and early sunset gold, settling premium tone.",
  FIN: "GRADE: FIN — rich golden warm hero-shot tone, premium and triumphant.",
};

// ref: "face" | "product" | "both" | null
const CUTS = [
  [1, "AWAY", "face", "Extreme close-up of a young blonde woman in her early 20s waking up to an alarm at dawn, tired bleary expression, cramped bedroom, no makeup, no logos."],
  [2, "AWAY", null, "A cluttered bed covered in an open laptop, scattered sticky notes and papers, dawn light, nobody's face visible, evidence of overwork."],
  [3, "AWAY", "face", "The young blonde woman in front of a mirror fixing her hair, exhaling a tired sigh, premium minimal bathroom, cool blue light."],
  [4, "AWAY", null, "A window with blinds, pale cold dawn light filtering through, empty room, melancholic mood, no people."],
  [5, "AWAY", null, "A desk with a cold abandoned coffee cup and an unfinished sketch/document, dawn light, nobody visible, sense of weight and pressure."],
  [6, "AWAY", "face", "The young blonde woman packing a bag, glancing at the mirror but avoiding her own reflection's gaze, cool blue tone, self-distant mood."],
  [7, "AWAY", "face", "The young blonde woman leaving her apartment, phone buzzing with notifications she ignores, cool dawn light in the hallway."],
  [8, "AWAY", "product", "A premium energy drink can sitting untouched on the corner of a cluttered desk, cold dawn light, nobody paying attention to it, quietly present."],
  [9, "WARM", "face", "The young blonde woman arriving at a busy creative workspace/cafe, soft bokeh of a bustling street behind her, light starting to warm."],
  [10, "WARM", "face", "Close-up of the young blonde woman rubbing her tired eyes while working intensely at a desk, warming tungsten light creeping in."],
  [11, "WARM", "face", "The young blonde woman pausing for a brief breath, looking out a window mid-work, soft warm light, quiet exhaustion."],
  [12, "WARM", "both", "The young blonde woman noticing the energy drink can on her desk for the first time, a moment of quiet recognition, warm tungsten light beginning to glow."],
  [13, "WARM", "both", "Extreme close-up of hands cracking open the energy drink can, light mist rising, condensation droplets, warm light."],
  [14, "WARM", "both", "The young blonde woman taking a sip of the energy drink, her tense expression softening slightly, a small moment of relief, warm light."],
  [15, "WARM", "face", "The young blonde woman diving back into her work with renewed energy, hands moving quickly across a keyboard, warm tungsten light."],
  [16, "WARM", "face", "The young blonde woman walking down a city street, light growing warmer as the afternoon progresses, dynamic urban bokeh."],
  [17, "WARM", "face", "A brief warm interaction with a colleague, shown only as a blurred silhouette/back and a hand gesture, the woman's face dominant and in focus."],
  [18, "WARM", "face", "Close-up of the young blonde woman's hands closing a laptop on a finished piece of work, a small sense of accomplishment, warm light."],
  [19, "HOME", "face", "The young blonde woman standing by a window at sunset, warm tungsten and golden light pouring in, a shift in mood toward calm."],
  [20, "HOME", "face", "The young blonde woman packing up her things with a small genuine smile, warm golden light, a sign of recovery."],
  [21, "HOME", "face", "The young blonde woman in front of a mirror again, this time meeting her own gaze with quiet reconciliation, warm golden light."],
  [22, "HOME", "both", "Close-up of the young blonde woman's hand holding the now-empty energy drink can as she tidies her desk, a quiet moment of recognition of its presence through the day."],
  [23, "HOME", "face", "A golden-hour backlit silhouette of the young blonde woman walking home, warm rim light tracing her figure, a sense of release."],
  [24, "HOME", "face", "The young blonde woman pausing at her front door, taking a deep breath in profile, golden light, arriving at a meaningful finish line."],
  [25, "FIN", "product", "The energy drink can resting on a windowsill in rich golden evening light, rim-lit, a quiet companion at day's end."],
  [26, "FIN", "product", "Extreme macro close-up of the energy drink can's design — abstract vertical wordmark and brushed-silver lightning emblem, golden hero light, demai bokeh."],
  [27, "FIN", "product", "Macro close-up of condensation droplets rolling down the energy drink can, golden rim light, premium texture detail."],
  [28, "FIN", "both", "Close-up of the young blonde woman's hand lifting the energy drink can, echoing the opening cut as a match-cut, golden hero light."],
  [29, "FIN", "product", "A wide brand mood shot of the energy drink can with a golden sunset visible through a window behind it, premium atmosphere, negative space left for a logo."],
  [30, "FIN", "product", "The energy drink can alone as a final hero shot, deep controlled shadows with golden rim light, ample negative space reserved for the logo."],
];

function buildPrompt(scene, grade) {
  return `${scene}\n${RULE0_IMG}\n${IMG_ENHANCE}\n${GRADE[grade]}`;
}

function refArgs(refType) {
  if (refType === "face") return ["--image", REF_FACE];
  if (refType === "product") return ["--image", REF_PRODUCT];
  if (refType === "both") return ["--image", REF_FACE, "--image", REF_PRODUCT];
  return [];
}

async function generateCut([num, act, refType, scene]) {
  const outPath = join(IMG_DIR, `cut_${String(num).padStart(2, "0")}.png`);
  if (existsSync(outPath)) {
    console.log(`[skip] cut ${num} already exists`);
    return;
  }
  const prompt = buildPrompt(scene, act);
  const args = [
    "-y", "-p", "@higgsfield/cli", "higgsfield",
    "generate", "create", "nano_banana_2",
    "--prompt", prompt,
    ...refArgs(refType),
    "--aspect_ratio", "16:9",
    "--resolution", "2k",
    "--wait", "--wait-timeout", "5m",
  ];
  console.log(`[gen] cut ${num} (act ${act}, ref ${refType ?? "none"})…`);
  try {
    const { stdout } = await execFileP("npx", args, { maxBuffer: 1024 * 1024 * 10 });
    const url = stdout.trim().split("\n").pop();
    console.log(`[done] cut ${num} -> ${url}`);
    const res = await fetch(url);
    const buf = Buffer.from(await res.arrayBuffer());
    await import("node:fs/promises").then((fs) => fs.writeFile(outPath, buf));
    console.log(`[saved] cut ${num} -> ${outPath}`);
  } catch (err) {
    console.error(`[error] cut ${num}:`, err.message);
  }
}

async function main() {
  for (const cut of CUTS) {
    await generateCut(cut);
  }
  console.log("=== ALL CUTS DONE ===");
}

main();
