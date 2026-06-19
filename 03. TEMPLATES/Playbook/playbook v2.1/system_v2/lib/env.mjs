import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = path.resolve(__dirname, '..', '.env');
const ROOT = path.resolve(__dirname, '..', '..');

export function loadEnv() {
  if (!fs.existsSync(ENV_PATH)) return;
  const text = fs.readFileSync(ENV_PATH, 'utf8');
  for (const line of text.split('\n')) {
    const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
  }
}

export function required(name) {
  const v = process.env[name];
  if (!v) throw new Error(`env var ${name} required`);
  return v;
}

export function todayVersion() {
  return 'v' + new Date().toISOString().slice(0, 10);
}

export function projectPaths(project, version, kind) {
  // 경로 규칙: projects/{project}/{version}/{kind} — type 층 없음.
  const dir = path.join(ROOT, 'projects', project, version, kind);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

export { ROOT };
