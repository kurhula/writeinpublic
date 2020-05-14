web: bin/prestart.sh gunicorn writeit.wsgi  --worker-class gevent --log-file - -b 0.0.0.0:5000
worker: celery -A writeit worker
beat: celery -A writeit beat --pidfile= -s /var/celerybeat/celerybeat-schedule
