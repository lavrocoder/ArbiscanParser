:: Переходим в текущую директорию (с .bat файлами).
cd /d %~dp0
:: Переходим в директорию выше, туда где основной код.
cd ..
:: Сохраняем путь в переменную root.
set root=%CD%
:: Записываем название виртуального окружения в переменную env_name.
set env_name=venv
:: Создаём виртуальное окружение.
python -m venv %env_name%
:: Обновляем pip в виртуальном окружении.
"%root%\%env_name%\Scripts\python.exe" -m pip install --upgrade pip
:: Устанавливаем зависимости.
"%root%\%env_name%\Scripts\pip.exe" install -r "requirements.txt"