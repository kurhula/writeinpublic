#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python manage.py compilemessages
python manage.py collectstatic --noinput

exec "$@"
