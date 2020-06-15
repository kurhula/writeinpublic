web: bin/prestart.sh gunicorn writeit.wsgi -w 3 --log-level=debug --log-file - -t 600 -b 0.0.0.0:5000
worker: celery -A writeit worker
beat: celery -A writeit beat --pidfile= -s /var/celerybeat/celerybeat-schedule
