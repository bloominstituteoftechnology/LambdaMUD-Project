web: gunicorn adv_project.wsgi:application --log-file -
release: python manage.py makemigrations --noinput && python manage.py migrate --noinput