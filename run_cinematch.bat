@echo off
title CineMatch Movie Recommender
cd /d "C:\Users\Nucom\Projects\MovieRecommender"

echo =========================================================
echo       Starting CineMatch Movie Recommender...
echo =========================================================
echo.
echo [1] Local access:  http://localhost:8501
echo [2] Generating your zero-password public sharing link...
echo.

python launch_public.py

pause
