#!/usr/bin/env bash
# 플레이북 리뷰 서버 재시작 스크립트
# 실행: bash start_servers.sh  (playbook v2.1/ 루트에서)

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

start_server() {
  local PROJECT=$1
  local VERSION=$2
  local PORT=$3
  local LOG="/tmp/review_server_$(echo "$PROJECT" | tr '[:upper:]' '[:lower:]').log"

  # 기존 프로세스 종료
  if lsof -ti :"$PORT" &>/dev/null; then
    echo "  [${PROJECT}] 포트 ${PORT} 기존 프로세스 종료..."
    kill "$(lsof -ti :"$PORT")" 2>/dev/null || true
    sleep 0.5
  fi

  # 백그라운드 시작
  nohup python3 "$ROOT/system_v2/_review_server.py" \
    --project "$PROJECT" \
    --version "$VERSION" \
    --port "$PORT" \
    > "$LOG" 2>&1 &
  local PID=$!

  # 확인
  sleep 1.5
  if curl -s "http://localhost:${PORT}/api/status" | grep -q '"ok": true'; then
    echo "  ✓ ${PROJECT}  http://localhost:${PORT}  PID=${PID}"
  else
    echo "  ✗ ${PROJECT} 시작 실패 — 로그: ${LOG}"
  fi
}

echo ""
echo "▐ Playbook Review Servers — 시작"
echo ""

start_server "VELVET_NOIR"  "v20260626"  7800
start_server "COFFEE_WAIT"  "v20260626"  7801

echo ""
echo "종료: kill \$(lsof -ti :7800 :7801)"
echo ""
