FROM bitnami/python:3.13.3-debian-12-r13

ARG NEW_LX_USER_GRP_GID='1010'
ARG NEW_LX_USER_GRP_NAME='tolteques'
ARG NEW_LX_USER_NAME='tolt'
ARG NEW_LX_USER_UID='1000'

RUN apt-get update -y && apt-get install -y ffmpeg

RUN mkdir -p /tolt/app
WORKDIR /tolt
COPY create.lx.user.sh .
RUN chmod a+x ./create.lx.user.sh && ./create.lx.user.sh
COPY install.miniconda.sh .
RUN chmod a+x ./install.miniconda.sh

RUN chown $NEW_LX_USER_NAME:$NEW_LX_USER_GRP_NAME -R /tolt

USER $NEW_LX_USER_NAME
RUN ./install.miniconda.sh

RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
    bash -c 'echo "in docker build, check conda install:" && source ~/.bashrc && conda --version'
RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
    conda --version

COPY VoyageVocab.py /tolt/app/
COPY environment.yml /tolt/app/
WORKDIR /tolt/app

RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
    conda env create -f environment.yml

RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
    conda init bash

RUN echo "export PATH='\$PATH:\$HOME/anaconda3/bin' && conda activate tolt_env" > ~/.bashrc
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     conda activate tolt_env

# SHELL ["conda", "activate", "tolt_env"]
# RUN . ~/.bashrc && conda --version
# RUN . ~/.bashrc && conda create -n tolt_env llm && conda activate llm


# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     bash -c 'echo "check in conda activated env: " && source ~/.bashrc && conda --version && python --version && pip -V'
SHELL ["conda", "run", "-n", "tolt_env", "/bin/bash", "-c","conda --version && python --version && pip -V"]
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     python --version
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     pip -V




# ---
# That's for CPU, not CUDA, not ROCm
SHELL ["conda", "run", "-n", "tolt_env", "/bin/bash", "-c","pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"]
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


# ---
# Install Whisper
# RUN pip install git+https://github.com/openai/whisper.git
# RUN pip install -U openai-whisper
SHELL ["conda", "run", "-n", "tolt_env", "/bin/bash", "-c","pip install openai-whisper"]
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     pip install openai-whisper
# ---

SHELL ["conda", "run", "-n", "tolt_env", "/bin/bash", "-c","pip install gradio"]
# RUN export PATH="$PATH:$HOME/anaconda3/bin" && \
#     pip install gradio


EXPOSE 7860

# CMD [ "python", "VoyageVocab.py" ]
ENTRYPOINT ["/bin/bash", "-c", "conda", "run", "--no-capture-output", "-n", "tolt_env", "python", "VoyageVocab.py"]