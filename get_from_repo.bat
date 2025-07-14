@echo off
setlocal

REM === Configurable Variables ===

set REPO_URL=https://github.com/Kisara-k/course-notes.git

set FOLDER_PATH=coursera/02 Deep Learning Specialization

set DEST_DIR=output
set TEMP_DIR=temp_repo

REM Get the directory where the script is running from
set SCRIPT_DIR=%~dp0

REM Clean up any previous temp directory
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"

REM Initialize and configure sparse-checkout
git init "%TEMP_DIR%"
cd "%TEMP_DIR%"
git remote add -f origin %REPO_URL%
git config core.sparseCheckout true
echo %FOLDER_PATH%/ > .git\info\sparse-checkout

REM Pull only the target folder
git pull origin main

REM Create destination directory if it doesn't exist
mkdir "..\%DEST_DIR%"

REM MOVE contents to the destination directory
move "%FOLDER_PATH%\*" "..\%DEST_DIR%\" >nul

REM If Lectures.json exists, move it to the script directory
if exist "..\%DEST_DIR%\Lectures.json" (
    move "..\%DEST_DIR%\Lectures.json" "%SCRIPT_DIR%" >nul
    echo Moved Lectures.json to %SCRIPT_DIR%
)

REM Clean up
cd ..
rmdir /s /q "%TEMP_DIR%"

echo Done! Folder "%FOLDER_PATH%" moved to "%DEST_DIR%"
endlocal