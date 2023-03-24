:: Получаем текущую директорию
cd /d %~dp0
cd ..
set root=%CD%
:: Название виртуального окружения
set env_name=venv
:: Название запускаемого python скрипта
set script_name=main.py
:: Переходим в папку проекта
cd %root%
:: Запускаем скрипт
"%root%\%env_name%\Scripts\python.exe" "%script_name%"