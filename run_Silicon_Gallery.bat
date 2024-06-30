@echo off
cd /d %~dp0
xcopy /s /e /i /d /q %~dp0\SiliconUI %~dp0\.venv\Lib\site-packages\SiliconUI
cd examples\Gallery
%~dp0\.venv\Scripts\python.exe start.py
