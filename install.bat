@echo off
cd ..
REM copy the "webx-extension" dir to ~/.vscode/extensions/
xcopy /E /Y /I "webx-extension" "%USERPROFILE%\.vscode\extensions\webx-extension"
cd "webx-extension"