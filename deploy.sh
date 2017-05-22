#!/bin/bash
export DJANGO_SETTINGS_MODULE='fair_health.settings.prod'
python manage.py collectstatic --clear --noinput
zappa update prod
