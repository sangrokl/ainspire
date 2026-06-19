@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo [AETHER] 스토리보드 이미지 리뷰 콘솔을 시작합니다...
python start.py --media-dir "..\v2026-05-29_v4" --mode image --title "AETHER 스토리보드 리뷰" %*
pause
