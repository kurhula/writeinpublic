FROM python:2.7

ENV PYTHONUNBUFFERED 1

COPY pkglist /tmp/
RUN apt-get update \
  && apt-get install -y $(cat /tmp/pkglist) \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy, then install requirements before copying rest for a requirements cache layer.
COPY requirements.txt /tmp/
RUN cd /tmp \
    && pip install -r requirements.txt

COPY . /app
python manage.py compilemessages
python manage.py collectstatic --noinput

RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && mkdir -p /var/celerybeat /var/coverage\
    && chown -R django:django /var /app
USER django

WORKDIR /app

EXPOSE 5000
CMD /app/bin/start.sh