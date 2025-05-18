#!/bin/bash

export PATH="$PATH:$HOME/anaconda3/bin"

bash -c 'conda run --no-capture-output -n tolt_env python VoyageVocab.py'