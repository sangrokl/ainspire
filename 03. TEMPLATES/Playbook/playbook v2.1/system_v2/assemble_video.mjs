// Assemble final ad video from scene clips + BGM using cut_plan.json.
// Required env: PROJECT
// Optional: VERSION, OUT_NAME (default bag_ad_final), OUT_SUBDIR (default final/v1),
//           BGM_PATH (default audio/bag_ad_bgm_final.mp3),
//           SOURCE_MAP (JSON mapping scene number → relative path under videos/scenes/)
//
// Pipeline:
//   1. For each scene: probe source duration, setpts-scale to target duration, -t truncate.
//   2. ffmpeg concat all scaled clips into single video stream.
//   3. Mix BGM audio track via ffmpeg (re-encode audio to aac, copy video).

import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
import { loadEnv, required, todayVersion, projectPaths, ROOT } from './lib/env.mjs';
import { appendManualOp } from './lib/log.mjs';

loadEnv();

const PROJECT = required('PROJECT');
const VERSION = process.env.VERSION || todayVersion();
const OUT_NAME = process.env.OUT_NAME || 'bag_ad_final';
const OUT_SUBDIR = process.env.OUT_SUBDIR || 'final/v1';

const projectRoot = path.join(ROOT, 'projects', PROJECT, VERSION);
const cutPlanPath = path.join(projectRoot, 'text', 'cut_plan.json');
const bgmPath = process.env.BGM_PATH
  ? (path.isAbsolute(process.env.BGM_PATH) ? process.env.BGM_PATH : path.join(ROOT, process.env.BGM_PATH))
  : path.join(projectRoot, 'audio', 'bag_ad_bgm_final.mp3');

if (!fs.existsSync(cutPlanPath)) throw new Error(`cut_plan.json not found at ${cutPlanPath}`);
if (!fs.existsSync(bgmPath)) throw new Error(`BGM not found at ${bgmPath}`);

const cutPlan = JSON.parse(fs.readFileSync(cutPlanPath, 'utf8'));

// Default source map for bag_ad project (from_keys/v2 9개 + from_gpt/v1 scene 6)
const defaultMap = {
  1: 'from_keys/v2/scene_01_hook.mp4',
  2: 'from_keys/v2/scene_02_pickup.mp4',
  3: 'from_keys/v2/scene_03_wear.mp4',
  4: 'from_keys/v2/scene_04_walking.mp4',
  5: 'from_keys/v2/scene_05_entry.mp4',
  6: 'from_gpt/v1/scene_06_gallery.mp4',
  7: 'from_keys/v2/scene_07_detail.mp4',
  8: 'from_keys/v2/scene_08_playful.mp4',
  9: 'from_keys/v2/scene_09_lifestyle.mp4',
  10: 'from_keys/v2/scene_10_endcard.mp4',
};
const sourceMap = process.env.SOURCE_MAP ? JSON.parse(process.env.SOURCE_MAP) : defaultMap;

const finalDir = path.join(projectRoot, 'videos', OUT_SUBDIR);
const tmpDir = path.join(finalDir, 'tmp');
fs.mkdirSync(tmpDir, { recursive: true });

function run(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'] });
  if (r.status !== 0) {
    process.stderr.write(r.stderr?.toString() || '');
    throw new Error(`${cmd} exited with ${r.status}`);
  }
  return r;
}

function probeDuration(file) {
  const r = spawnSync('ffprobe', ['-v', 'quiet', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file]);
  return parseFloat(r.stdout.toString().trim());
}

// 1. Scale each scene
console.log('=== scaling scenes ===');
for (const s of cutPlan.scenes) {
  const srcRel = sourceMap[s.scene];
  if (!srcRel) throw new Error(`no source for scene ${s.scene}`);
  const srcAbs = path.join(projectRoot, 'videos', 'scenes', srcRel);
  if (!fs.existsSync(srcAbs)) throw new Error(`source not found: ${srcAbs}`);
  const srcDur = probeDuration(srcAbs);
  const factor = s.duration / srcDur;
  const scaledPath = path.join(tmpDir, `scene_${String(s.scene).padStart(2, '0')}.mp4`);
  console.log(`  scene ${s.scene}: ${srcRel} (${srcDur.toFixed(3)}s) → ${s.duration}s (setpts factor=${factor.toFixed(4)})`);
  run('ffmpeg', [
    '-y', '-i', srcAbs,
    '-filter:v', `setpts=${factor.toFixed(6)}*PTS`,
    '-an',
    '-t', s.duration.toString(),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-pix_fmt', 'yuv420p',
    scaledPath,
  ]);
}

// 2. Concat
console.log('\n=== concatenating ===');
const concatList = cutPlan.scenes
  .map(s => `file '${path.join(tmpDir, `scene_${String(s.scene).padStart(2, '0')}.mp4`).replace(/\\/g, '/')}'`)
  .join('\n');
const concatPath = path.join(tmpDir, 'concat.txt');
fs.writeFileSync(concatPath, concatList);

const videoOnly = path.join(tmpDir, 'video_only.mp4');
run('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', concatPath, '-c', 'copy', videoOnly]);
console.log(`  video_only: ${probeDuration(videoOnly).toFixed(3)}s`);

// 3. Mix BGM
console.log('\n=== mixing BGM ===');
const finalPath = path.join(finalDir, `${OUT_NAME}.mp4`);
run('ffmpeg', [
  '-y',
  '-i', videoOnly,
  '-i', bgmPath,
  '-map', '0:v', '-map', '1:a',
  '-c:v', 'copy',
  '-c:a', 'aac', '-b:a', '192k',
  '-shortest',
  finalPath,
]);

const finalDur = probeDuration(finalPath);
const finalSize = fs.statSync(finalPath).size;
console.log(`\n✅ Assembled: ${finalPath}`);
console.log(`   Duration: ${finalDur.toFixed(3)}s`);
console.log(`   Size: ${(finalSize / 1024 / 1024).toFixed(2)} MB`);

appendManualOp(PROJECT, VERSION, 'edit/final-assembly', 'ffmpeg_concat_bgm_mix', {
  source_map: sourceMap,
  cut_plan: path.relative(ROOT, cutPlanPath).replace(/\\/g, '/'),
  bgm: path.relative(ROOT, bgmPath).replace(/\\/g, '/'),
  output: path.relative(ROOT, finalPath).replace(/\\/g, '/'),
  final_duration_sec: +finalDur.toFixed(3),
  final_size_mb: +(finalSize / 1024 / 1024).toFixed(2),
});
