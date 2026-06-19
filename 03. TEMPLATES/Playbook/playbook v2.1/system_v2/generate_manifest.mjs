// Build tools/dashboard.html manifest from a project version folder.
// Required env: PROJECT
// Optional env: VERSION

import fs from 'fs';
import path from 'path';
import { loadEnv, required, todayVersion, ROOT } from './lib/env.mjs';

loadEnv();

const PROJECT = required('PROJECT');
const VERSION = process.env.VERSION || todayVersion();
const projectRoot = path.join(ROOT, 'projects', PROJECT, VERSION);
const manifestPath = path.join(projectRoot, 'manifest.json');

const IMAGE_EXT = new Set(['.png', '.jpg', '.jpeg', '.webp']);
const VIDEO_EXT = new Set(['.mp4', '.mov', '.webm']);
const AUDIO_EXT = new Set(['.mp3', '.wav', '.m4a', '.aac']);

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(abs));
    else out.push(abs);
  }
  return out;
}

function rel(abs) {
  return path.relative(projectRoot, abs).replace(/\\/g, '/');
}

function mediaKind(file) {
  const ext = path.extname(file).toLowerCase();
  if (IMAGE_EXT.has(ext)) return 'images';
  if (VIDEO_EXT.has(ext)) return 'videos';
  if (AUDIO_EXT.has(ext)) return 'audio';
  return null;
}

function inferCutId(file) {
  const base = path.basename(file, path.extname(file)).toLowerCase();
  const sceneCut = base.match(/(?:scene|s)[_-]?(\d+).*?(?:cut|c)[_-]?(\d+)/);
  if (sceneCut) return `${Number(sceneCut[1])}-${Number(sceneCut[2])}`;
  const explicitCut = base.match(/(?:cut|c)[_-]?(\d+)[_-](\d+)/);
  if (explicitCut) return `${Number(explicitCut[1])}-${Number(explicitCut[2])}`;
  const sceneOnly = base.match(/(?:scene|s)[_-]?(\d+)/);
  if (sceneOnly) return `${Number(sceneOnly[1])}-1`;
  return 'misc-1';
}

function sceneIdFromCut(cutId) {
  const n = String(cutId).split('-')[0];
  return /^\d+$/.test(n) ? `s${n}` : 'misc';
}

function sortByName(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
}

function loadExisting() {
  if (!fs.existsSync(manifestPath)) return null;
  try {
    return JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch {
    return null;
  }
}

function existingCutMeta(existing) {
  const meta = new Map();
  for (const scene of existing?.scenes || []) {
    for (const cut of scene.cuts || []) {
      meta.set(cut.id, { desc: cut.desc || '', sceneTitle: scene.title || '' });
    }
  }
  return meta;
}

if (!fs.existsSync(projectRoot)) {
  throw new Error(`project version folder not found: ${projectRoot}`);
}

const existing = loadExisting();
const meta = existingCutMeta(existing);
const cuts = new Map();

for (const file of walk(projectRoot)) {
  const kind = mediaKind(file);
  if (!kind) continue;
  const relative = rel(file);
  if (relative.startsWith('refs/')) continue;
  const cutId = inferCutId(file);
  if (!cuts.has(cutId)) {
    cuts.set(cutId, { id: cutId, desc: meta.get(cutId)?.desc || '', images: [], videos: [], audio: [] });
  }
  cuts.get(cutId)[kind].push(relative);
}

const scenesById = new Map();
for (const cut of [...cuts.values()].sort((a, b) => sortByName(a.id, b.id))) {
  cut.images.sort(sortByName);
  cut.videos.sort(sortByName);
  cut.audio.sort(sortByName);
  const sceneId = sceneIdFromCut(cut.id);
  if (!scenesById.has(sceneId)) {
    const title = meta.get(cut.id)?.sceneTitle || '';
    scenesById.set(sceneId, { id: sceneId, title, cuts: [] });
  }
  scenesById.get(sceneId).cuts.push(cut);
}

const manifest = {
  project: existing?.project || PROJECT,
  version: VERSION,
  scenes: [...scenesById.values()].sort((a, b) => sortByName(a.id, b.id)),
};

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n');
console.log(`[manifest] wrote ${path.relative(ROOT, manifestPath).replace(/\\/g, '/')}`);
