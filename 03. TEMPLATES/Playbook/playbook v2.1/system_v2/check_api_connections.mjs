import { loadEnv } from './lib/env.mjs';

loadEnv();

// MCP 전용 파이프라인 — 이 스크립트는 ElevenLabs(내레이션, 유일한 직접 키)만 점검한다.
//   · 이미지·영상 생성 = MCP 엔진(Higgsfield / Magnific) — 둘 다 OAuth, 별도 키 불필요(스크립트로 점검 불가).
//       크레딧: Higgsfield = MCP `balance`, Magnific = MCP `account_balance`.
//   · 내레이션(VO) = ElevenLabs 직접 API (유일한 키, 선택).

const checks = [
  {
    name: 'ElevenLabs',
    url: 'https://api.elevenlabs.io/v1/user',
    keyVar: 'ELEVENLABS_API_KEY',
    headers: () => ({ 'xi-api-key': process.env.ELEVENLABS_API_KEY }),
    optional: true,
  },
];

async function check({ name, url, keyVar, headers, optional }) {
  const token = process.env[keyVar];
  if (!token) {
    if (optional) {
      console.log(`${name}: SKIP (no ${keyVar})`);
      return true;
    }
    console.log(`${name}: MISSING ${keyVar}`);
    return false;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const response = await fetch(url, { headers: headers(), signal: controller.signal });

    if (response.ok) {
      console.log(`${name}: OK (HTTP ${response.status})`);
      return true;
    }

    if (response.status === 401 || response.status === 403) {
      console.log(`${name}: AUTH FAILED (HTTP ${response.status})`);
      return false;
    }

    console.log(`${name}: CHECK FAILED (HTTP ${response.status})`);
    return false;
  } catch (error) {
    const reason = error.name === 'AbortError' ? 'timeout' : error.message;
    console.log(`${name}: NETWORK FAILED (${reason})`);
    return false;
  } finally {
    clearTimeout(timeout);
  }
}

console.log('[check] 생성 엔진은 MCP(OAuth): Higgsfield(`balance`) / Magnific(`account_balance`) — 스크립트 점검 불가');

const results = await Promise.all(checks.map(check));

if (results.some((ok) => !ok)) {
  process.exitCode = 1;
}
