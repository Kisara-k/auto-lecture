@echo off
echo ==== 1 Merging slides ====
python 1_merge_slides.py
echo.

echo ==== 2 Extracting content ====
python 2_extract_content.py
echo.

echo ==== 3 Calling API ====
python 3_call_api.py
echo.

echo All steps completed.
pause
