#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda. (this does not work at all)

# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

source ~/.bashrc

export PATH="$PATH:$HOME/anaconda3/bin"


# Enable strict mode.
# set -euo pipefail

conda --version
# ... Run whatever commands ...

# Temporarily disable strict mode and activate conda:
# set +euo pipefail
# conda init
# conda activate tolt_env

# Re-enable strict mode:
# set -euo pipefail


# conda run -n tolt_env /bin/bash -c 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
#   pip install git+https://github.com/openai/whisper.git && \
#   python VoyageVocab.py'
# conda run -n tolt_env /bin/bash -c '/tolt/app/install.py.dependencies.sh'
# conda run -n tolt_env /bin/bash -c 'python VoyageVocab.py'
python VoyageVocab.py
# python VoyageVocab.py