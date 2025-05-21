import whisper
import torch

class WhisperService:
    """A simple example class"""

    # whisper_model = 12345
    whisper_model_name = 'medium'
    whisper_model = None
    def __init__(self):
      self.whisper_model_name = 'medium'
      self.whisper_model = whisper.load_model(self.whisper_model_name)
    def some_method(self):
        return 'hello world'

# service = WhisperService() # Will this be static once and for all ??

# def jbl_test(audio_file):
def transcribe_audio(audio_file):
    cheminFichier =   "Donc voilà le audio_file: [%s]" % audio_file
    print(" Donc voilà le audio: [%s]", audio_file)
    # testFIchier = '/c/Users/Utilisateur/AppData/Local/Temp/gradio/f4d2ba5e63db118ad186d35d1aa2b50ffe8325422d9e5e4963c93eb66a373e94/audio.wav'
    # resultat = transcribe_audio(testFIchier)
    # resultat = transcribe_audio(audio_file)
    # return "%s is %s" % (cheminFichier, resultat)
    # model = whisper.load_model("base")
    model = whisper.load_model("medium")
    print (" POKUS in jbl_test the  is %s", audio_file)
    audio = whisper.load_audio(audio_file,sr=16000)
    audio_tensor = torch.from_numpy(audio).to(torch.float32)
    result = model.transcribe(audio_tensor, fp16=False)['text']
    print (" POKUS in jbl_test before returning the transcribed text: the transcribed text is %s", result)
    return result

##############################
###### DEPENDENCIES CONFIRMED IN A CONDA ENV:
# 
# (tolt_env) tolt@a7b13a545e6d:/tolt/app$ pip show torchaudio
# Name: torchaudio
# Version: 2.7.0+cpu
# Summary: An audio package for PyTorch
# Home-page: https://github.com/pytorch/audio
# Author: Soumith Chintala, David Pollack, Sean Naren, Peter Goldsborough, Moto Hira, Caroline Chen, Jeff Hwang, Zhaoheng Ni, Xiaohui Zhang
# Author-email: soumith@pytorch.org
# License:
# Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
# Requires: torch
# Required-by:
# (tolt_env) tolt@a7b13a545e6d:/tolt/app$ pip show torchvision
# Name: torchvision
# Version: 0.22.0+cpu
# Summary: image and video datasets and models for torch deep learning
# Home-page: https://github.com/pytorch/vision
# Author: PyTorch Core Team
# Author-email: soumith@pytorch.org
# License: BSD
# Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
# Requires: numpy, pillow, torch
# Required-by:
# (tolt_env) tolt@a7b13a545e6d:/tolt/app$ pip show torch
# Name: torch
# Version: 2.7.0+cpu
# Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
# Home-page: https://pytorch.org/
# Author: PyTorch Team
# Author-email: packages@pytorch.org
# License: BSD-3-Clause
# Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
# Requires: filelock, fsspec, jinja2, networkx, setuptools, sympy, typing-extensions
# Required-by: openai-whisper, torchaudio, torchvision
# (tolt_env) tolt@a7b13a545e6d:/tolt/app$ pip show openai-whisper
# Name: openai-whisper
# Version: 20240930
# Summary: Robust Speech Recognition via Large-Scale Weak Supervision
# Home-page: https://github.com/openai/whisper
# Author: OpenAI
# Author-email:
# License: MIT
# Location: /home/tolt/anaconda3/envs/tolt_env/lib/python3.13/site-packages
# Requires: more-itertools, numba, numpy, tiktoken, torch, tqdm, triton
# Required-by:
# (tolt_env) tolt@a7b13a545e6d:/tolt/app$
