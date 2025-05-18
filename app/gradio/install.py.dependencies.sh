#!/bin/bash

# ---
# That's for CPU, not CUDA, not ROCm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install openai-whisper

# pip install gradio langchain langchain-community