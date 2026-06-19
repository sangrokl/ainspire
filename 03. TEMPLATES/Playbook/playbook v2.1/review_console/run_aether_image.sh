#!/usr/bin/env bash
# AETHER 스토리보드 이미지 리뷰 콘솔 (mac/linux)
cd "$(dirname "$0")"
python3 start.py --media-dir "../v2026-05-29_v4" --mode image --title "AETHER 스토리보드 리뷰" "$@"
