#! /usr/bin/env bash

set -e
set -x

chmod +x ./prestart_whisper.sh
./prestart_whisper.sh

# Let the DB start
python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py
