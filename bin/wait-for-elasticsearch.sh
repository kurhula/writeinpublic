#!/bin/bash

elasticsearch_ready() {
    wget -q --waitretry=5 --retry-connrefused -T 10 -O - ELASTICSEARCH_URL
}

until elasticsearch_ready; do
  >&2 echo 'Waiting for elasticsearch to become available...'
  sleep 1
done
>&2 echo 'elasticsearch is available'

exec "$@"
