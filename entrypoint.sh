#!/usr/bin/env bash
set -e -o xtrace

sleep 5
python  manage.py migrate  --noinput || exit 1
python  create_superuser.py

exec "$@"
