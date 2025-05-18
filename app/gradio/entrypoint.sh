#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

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