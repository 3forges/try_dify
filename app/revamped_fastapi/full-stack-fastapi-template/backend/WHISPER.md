
```bash
(base) tolt@a7b13a545e6d:/tolt/app$ conda run -n tolt_env bash -c 'pip show torch'
Name: torch
Version: 2.7.0+cpu
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
Author: PyTorch Team
Author-email: packages@pytorch.org
License: BSD-3-Clause
Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
Requires: filelock, fsspec, jinja2, networkx, setuptools, sympy, typing-extensions
Required-by: openai-whisper, torchaudio, torchvision

(base) tolt@a7b13a545e6d:/tolt/app$ conda run -n tolt_env bash -c 'pip show torchvision'
Name: torchvision
Version: 0.22.0+cpu
Summary: image and video datasets and models for torch deep learning
Home-page: https://github.com/pytorch/vision
Author: PyTorch Core Team
Author-email: soumith@pytorch.org
License: BSD
Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
Requires: numpy, pillow, torch
Required-by:

(base) tolt@a7b13a545e6d:/tolt/app$ conda run -n tolt_env bash -c 'pip show torchaudio'
Name: torchaudio
Version: 2.7.0+cpu
Summary: An audio package for PyTorch
Home-page: https://github.com/pytorch/audio
Author: Soumith Chintala, David Pollack, Sean Naren, Peter Goldsborough, Moto Hira, Caroline Chen, Jeff Hwang, Zhaoheng Ni, Xiaohui Zhang
Author-email: soumith@pytorch.org
License:
Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
Requires: torch
Required-by:

(base) tolt@a7b13a545e6d:/tolt/app$ conda run -n tolt_env bash -c 'pip show openai-whisper'
Name: openai-whisper
Version: 20240930
Summary: Robust Speech Recognition via Large-Scale Weak Supervision
Home-page: https://github.com/openai/whisper
Author: OpenAI
Author-email:
License: MIT
Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
Requires: more-itertools, numba, numpy, tiktoken, torch, tqdm, triton
Required-by:

(base) tolt@a7b13a545e6d:/tolt/app$

```

I did:


```bash
# ---
# That's for CPU, not CUDA, not ROCm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# pip install openai-whisper
pip install git+https://github.com/openai/whisper.git


pip install langchain langchain-community

```

Ok all good except for torch and there i have an answer:

https://github.com/astral-sh/uv/issues/4173#issuecomment-2156715078

hm it seems installing torch is not easy with astral uv

https://docs.astral.sh/uv/reference/settings/#pip_torch-backend
