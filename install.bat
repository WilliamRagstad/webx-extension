@echo off
REM Compile syntax grammar files
py compile.py src/webx.tmLanguage.pre.json syntaxes/webx.tmLanguage.json

REM Install into VSCode
cd ..
REM copy the "webx-extension" dir to ~/.vscode/extensions/
xcopy /E /Y /I "webx-extension" "%USERPROFILE%\.vscode\extensions\webx-extension"
cd "webx-extension"