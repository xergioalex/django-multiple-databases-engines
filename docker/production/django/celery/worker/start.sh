#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

export C_FORCE_ROOT="true"
celery -A beyond_campus.taskapp worker -l INFO