# geoinformation-system
Проект для знакомства с основами геоинформатики: как работать с пространственными данными,
системами координат и отправлять запросы к БД

## Стек: 
Python, Django, Django REST Framework, PostgreSQL, PostGIS

## Инструкция по запуску:
- склонировать проект на свой компьютер
- создать, активировать виртуальное окружение
- установить необходимые пакеты для Python `pip install -r requirements.txt`
- установить необходимые программные пакеты \
`sudo apt-get install libgeos-dev` \
`sudo apt-get install binutils libproj-dev`\
`sudo apt-get install gdal-bin libgdal-dev`\
`sudo apt-get install python3-gdal`\
`sudo apt-get install postgresql`\
`sudo apt-get install postgresql-postgis`
- создать базу, подключиться к ней
- провести миграции
- запустить программу `python manage.py runserver`
