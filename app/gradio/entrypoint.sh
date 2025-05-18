#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda. (this does not work at all)

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

source ~/.bashrc

export PATH="$PATH:$HOME/anaconda3/bin"


# Enable strict mode.
set -euo pipefail

conda --version
# ... Run whatever commands ...

# Temporarily disable strict mode and activate conda:
set +euo pipefail
conda activate tolt_env

# Re-enable strict mode:
set -euo pipefail


python VoyageVocab.py
# python VoyageVocab.py