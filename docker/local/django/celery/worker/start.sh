#!/bin/sh

set -o errexit
set -o nounset

celery -A beyond_campus.taskapp worker -l INFO
