#!/usr/bin/env bash
PYTHONPATH=. DJANGO_SETTINGS_MODULE=sampleproject.settings py.test --create-db
