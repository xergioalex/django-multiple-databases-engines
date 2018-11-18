#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

# rm -f './celerybeat.pid'
celery -A beyond_campus.taskapp beat -l INFO
