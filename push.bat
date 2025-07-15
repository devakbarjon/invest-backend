@echo off
setlocal

:: Получаем дату и время
for /f "tokens=1-3 delims=/: " %%a in ("%date% %time%") do (
    set "datetime=%%a-%%b-%%c"
)

:: Сообщение коммита
set "COMMIT_MSG=Update For %datetime%"

:: Git-команды
git add .
git commit -m "%COMMIT_MSG%"
git push

exit
