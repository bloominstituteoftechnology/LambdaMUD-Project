web: gunicorn adv_project.wsgi:application --log-file -
worker: celery -A adv_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


