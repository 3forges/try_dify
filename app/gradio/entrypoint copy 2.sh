#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
source ~/.bashrc

export PATH="$PATH:$HOME/anaconda3/bin"

conda --version
conda run --no-capture-output -n tolt_env python VoyageVocab.py
# python VoyageVocab.py