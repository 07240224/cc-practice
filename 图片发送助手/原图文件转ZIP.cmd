@echo off
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0Pack-Images.ps1" -ChooseFiles
