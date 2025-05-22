#! /usr/bin/env bash

set -e
set -x

# chmod +x ./prestart_whisper.sh
# ./prestart_whisper.sh
# Pre loads the OpenAI Whisper model(s)
python app/whisper_pre_start.py

# Let the DB start
python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py
