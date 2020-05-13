web: gunicorn writeit.wsgi --log-file -
worker: celery -A writeit worker
beat: celery -A writeit beat --pidfile= -s /var/celerybeat/celerybeat-schedule
