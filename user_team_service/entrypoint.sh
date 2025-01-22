#!/bin/sh

# python manage.py flush --no-input

# python manage.py migrate


# Сборка статики
python manage.py collectstatic --no-input

# # Запуск Gunicorn
# gunicorn --bind 0.0.0.0:8000 config.wsgi:application

# Или для разработки с автоматической перезагрузкой:
exec python manage.py runserver 0.0.0.0:8000