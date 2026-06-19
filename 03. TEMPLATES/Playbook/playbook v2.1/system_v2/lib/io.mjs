import fs from 'fs';
import path from 'path';

const MIME = {
  png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
  webp: 'image/webp', gif: 'image/gif', bmp: 'image/bmp',
};

export function toDataUri(absPath) {
  const buf = fs.readFileSync(absPath);
  const ext = path.extname(absPath).toLowerCase().slice(1);
  const mime = MIME[ext] || 'image/png';
  return `data:${mime};base64,${buf.toString('base64')}`;
}

export async function saveFromUrl(url, outPath) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`download ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buf);
  return buf.length;
}

export function saveDataUri(dataUri, outPath) {
  const m = dataUri.match(/^data:([^;]+);base64,(.+)$/);
  if (!m) throw new Error('not a data URI');
  const buf = Buffer.from(m[2], 'base64');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, buf);
  return buf.length;
}

export const sleep = (ms) => new Promise(r => setTimeout(r, ms));
