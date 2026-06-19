import fs from 'fs';
import path from 'path';
import { ROOT } from './env.mjs';

export function sessionLogPath(project, version) {
  return path.join(ROOT, 'projects', project, version, 'text', 'session_log.md');
}

export function pipelineJsonlPath(project, version) {
  return path.join(ROOT, 'projects', project, version, 'text', 'pipeline.jsonl');
}

export function appendPipelineEvent(project, version, event) {
  const p = pipelineJsonlPath(project, version);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const enriched = { ts: new Date().toISOString(), ...event };
  fs.appendFileSync(p, JSON.stringify(enriched) + '\n');
}

export function appendUserInput(project, version, step, text, meta = {}) {
  appendPipelineEvent(project, version, { type: 'user_input', step, payload: { text, ...meta } });
}

export function appendUserFeedback(project, version, step, text, meta = {}) {
  appendPipelineEvent(project, version, { type: 'user_feedback', step, payload: { text, ...meta } });
}

export function appendUserDecision(project, version, step, decision, meta = {}) {
  appendPipelineEvent(project, version, { type: 'user_decision', step, payload: { decision, ...meta } });
}

export function appendStepMarker(project, version, step, phase, meta = {}) {
  appendPipelineEvent(project, version, { type: `step_${phase}`, step, payload: meta });
}

export function appendManualOp(project, version, step, op, meta = {}) {
  appendPipelineEvent(project, version, { type: 'manual_op', step, op, ...meta });
}

export function appendSession(project, version, entry) {
  const p = sessionLogPath(project, version);
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const ts = new Date().toISOString();
  const line = `\n### ${ts} — ${entry.step}\n` +
    `- **model**: ${entry.model}\n` +
    (entry.prompt ? `- **prompt**: \`${entry.prompt.replace(/`/g, "'").slice(0, 500)}${entry.prompt.length > 500 ? '...' : ''}\`\n` : '') +
    (entry.ref ? `- **ref**: ${entry.ref}\n` : '') +
    (entry.params ? `- **params**: ${JSON.stringify(entry.params)}\n` : '') +
    (entry.output ? `- **output**: ${entry.output}\n` : '') +
    (entry.predictionId ? `- **prediction_id**: ${entry.predictionId}\n` : '') +
    (entry.durationMs ? `- **took**: ${(entry.durationMs/1000).toFixed(1)}s\n` : '') +
    (entry.error ? `- **error**: ${entry.error}\n` : '') +
    (entry.note ? `- **note**: ${entry.note}\n` : '');
  fs.appendFileSync(p, line);

  // mirror into pipeline.jsonl as api_call event
  appendPipelineEvent(project, version, {
    type: 'api_call',
    step: entry.step,
    model: entry.model,
    prompt: entry.prompt || null,
    ref: entry.ref || null,
    params: entry.params || null,
    output: entry.output || null,
    prediction_id: entry.predictionId || null,
    duration_ms: entry.durationMs || null,
    error: entry.error || null,
    note: entry.note || null,
  });
}

export function writeSessionHeaderIfMissing(project, version, title) {
  const p = sessionLogPath(project, version);
  if (fs.existsSync(p)) return;
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const header = `# Session Log — ${project} ${version}\n\n` +
    `**목적**: ${title || '테스트 기록. 나중에 그대로 재현 가능하도록 각 호출의 input/output을 시간순으로 기록.'}\n\n` +
    `**재현 규칙**: 각 엔트리의 model + prompt + ref + params 조합을 그대로 호출하면 동일 결과(근사치) 재현.\n\n` +
    `---\n`;
  fs.writeFileSync(p, header);
}
