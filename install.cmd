@echo off
setlocal
cd /d "%~dp0"
set "HWP_INSTALL_PYTHON="
where py >nul 2>nul
if not errorlevel 1 set "HWP_INSTALL_PYTHON=py"
if defined HWP_INSTALL_PYTHON goto found
where python >nul 2>nul
if not errorlevel 1 set "HWP_INSTALL_PYTHON=python"
if defined HWP_INSTALL_PYTHON goto found
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" set "HWP_INSTALL_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if defined HWP_INSTALL_PYTHON goto found
echo Python was not found. Run install.py with your Python executable.
pause
exit /b 1
:found
"%HWP_INSTALL_PYTHON%" doctor.py
"%HWP_INSTALL_PYTHON%" install.py --check
if errorlevel 1 goto failed
"%HWP_INSTALL_PYTHON%" install.py
if errorlevel 1 goto failed
"%HWP_INSTALL_PYTHON%" install.py --status
if errorlevel 1 goto failed
echo Installation complete. Open a new Codex task and use $hwp.
pause
exit /b 0
:failed
echo Installation failed. Read the error above.
pause
exit /b 1
