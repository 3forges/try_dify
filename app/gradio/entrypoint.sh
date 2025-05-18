#!/bin/bash

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

conda --version
conda run --no-capture-output -n tolt_env python VoyageVocab.py
# python VoyageVocab.py