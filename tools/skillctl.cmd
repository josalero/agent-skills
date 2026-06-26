@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%"
if "%PYTHON%"=="" (
  set "PYTHON=python"
)
"%PYTHON%" -m skillforge.cli %*

