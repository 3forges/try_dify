#! /usr/bin/env bash

set -e
set -x

# Pre loads the OpenAI Whisper model(s)
python app/whisper_pre_start.py
