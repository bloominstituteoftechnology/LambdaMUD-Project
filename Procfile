web: gunicorn adv_project.wsgi:application --log-file -
worker: python manage.py celery worker -B -l info

