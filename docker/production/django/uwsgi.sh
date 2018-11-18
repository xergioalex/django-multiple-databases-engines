#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py collectstatic --noinput
python /app/manage.py migrate --noinput
/usr/local/bin/uwsgi --ini /app/uwsgi.ini --logto /app/uwsgi.log
