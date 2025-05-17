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

RUN . ~/.bashrc && conda --version
RUN . ~/.bashrc && conda create -n myenv llm && conda activate llm

RUN python3 --version 
RUN python --version
RUN pip3 -V


COPY VoyageVocab /tolt/app

WORKDIR /tolt/app


# ---
# That's for CPU, not CUDA, not ROCm
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


# ---
# Install Whisper
# RUN pip install git+https://github.com/openai/whisper.git
RUN pip install openai-whisper
# ---
RUN pip install gradio


EXPOSE 7860

CMD [ "python", "VoyageVocab.py" ]