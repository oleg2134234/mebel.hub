@echo off
cd /d "%~dp0"
echo Будут отправлены эти изменения:
git status --short
echo.
echo Закройте окно, если в списке есть лишнее. Иначе нажмите любую клавишу для отправки.
pause
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" end "Кордова 2 900: починен слайд Размеры; Реал Софт: слайд Размеры"
echo.
pause
