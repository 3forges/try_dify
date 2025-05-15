# Ollama

Ref.: https://www.arsturn.com/blog/using-ollama-for-automated-voice-transcription

```bash
export OLLAMA_IMG_GUN=docker.io/ollama/ollama
export OLLAMA_IMG_TAG=latest
# export OLLAMA_IMG_TAG='0.7.0'
# ---
# ROCM: that is for GPU
# export OLLAMA_IMG_TAG='0.7.0-rocm'

export CONTAINER_NAME="pesto-ollama"

export OLLAMA_HOME="/opt/ollama/home"
export OLLAMA_VOLUME=${OLLAMA_HOME}/volume
sudo mkdir -p ${OLLAMA_HOME}
sudo chown pesto:pesto -R /opt/ollama
mkdir -p ${OLLAMA_VOLUME}

cd ${OLLAMA_HOME}

docker run --name ${CONTAINER_NAME} \
 --restart unless-stopped \
 -itd -v ${OLLAMA_VOLUME}:/root/.ollama \
 -p 0.0.0.0:11434:11434 \
 ollama/ollama

docker exec -it ${CONTAINER_NAME}  bash -c 'pwd && ls -alh && pwd && id'
docker exec -it ${CONTAINER_NAME}  bash -c 'ollama --version'
docker exec -it ${CONTAINER_NAME}  bash -c 'ollama pull dimavz/whisper-tiny'

docker exec -it ${CONTAINER_NAME}  bash -c 'ollama run dimavz/whisper-tiny'

docker exec -it ${CONTAINER_NAME}  bash -c 'ollama pull llama2-uncensored'
docker exec -it ${CONTAINER_NAME}  bash -c 'ollama run llama2-uncensored'


# ---
# find avaialble models at https://ollama.com/
# https://ollama.com/dimavz/whisper-tiny


```

And I could check usage of OLLAMA API:

```bash

export MODEL_NAME='dimavz/whisper-tiny'

cat <<EOF >./PAYLOAD.json
{
   "model": "${MODEL_NAME}",
   "prompt": "Hey there ollama how coud I use you",
   "stream": false
}
EOF

export PAYLOAD=$(cat ./PAYLOAD.json) 
export OLLAMA_SERVICE_IPADDR="192.168.1.13"

curl -X POST -d ${PAYLOAD} -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate



export MODEL_NAME='dimavz/whisper-tiny'
cat <<EOF >./PAYLOAD.json
{
   "model": "${MODEL_NAME}"
}
EOF

export PAYLOAD=$(cat ./PAYLOAD.json) 

curl -X POST -d "${PAYLOAD}" -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/show

curl -X POST -d "${PAYLOAD}" -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/show | tail -n 1 | jq .

```

And also:

```bash

export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "llama2-uncensored", "prompt": "What is water made of?" }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate

```

And:

```bash
curl --location 'https://api.openai.com/v1/audio/transcriptions' \
--header 'Authorization: Bearer API_KEY' \
--form 'file=@"/home/bezbos/Downloads/english_recording_2.wav"' \
--form 'model="whisper-1"'

export MODEL_NAME='dimavz/whisper-tiny'
curl --location http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate \
--form 'file=@"./test/harvard.wav"' \
--form 'model="dimavz/whisper-tiny"'

export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "llama2-uncensored", "prompt": "What is water made of?" }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate





curl --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="dimavz%2Fwhisper-tiny"' http://192.168.1.13:11434/api/chat

# but with above iexperience same issue as https://github.com/go-swagger/go-swagger/issues/2491

```

https://github.com/ollama/ollama/blob/main/docs/api.md

https://www.arsturn.com/blog/using-ollama-for-automated-voice-transcription

* https://community.openai.com/t/calling-whisper-api-using-curl-request-keeps-giving-error/81510

* https://medium.com/@bezbos/openai-audio-whisper-api-guide-36e7272731dc


Ohhh see also: https://github.com/didevlab/audio-transcriber-whisper-api



Ok my problem with OLLAMA is that apparently i experience samae issue than others for integration with dify:

https://github.com/langgenius/dify-official-plugins/issues/498


So well, I will have, it seems, to try something else to be able to do speech to text, perhaps https://github.com/openai/whisper

There might be a good chance with : https://hub.docker.com/r/linuxserver/faster-whisper

## Ollama and GPUs

Refs:

* https://forum.openmandriva.org/t/ollama-rocm-for-amd-gpus/6801 , example hardware:
  * OpenMandriva Lx version: OpenMandriva Lx release 25.03 (ROME) Rolling for x86_64
  * Kernel version: 6.13.5-desktop-1omv2590
  * CPU: AMD Ryzen 5 3600 (12) @ 3.600GHz
  * GPU: AMD Radeon RX 6800 XT
  * GPU VBIOS version: 113-EXT48025-001
* Check how to use Ollama REST API: https://medium.com/@kevinnjagi83/exploring-ollama-rest-api-endpoints-7029fae5630d
* https://medium.com/@shmilysyg/setup-rest-api-service-of-ai-by-using-local-llms-with-ollama-eb4b62c13b71
* wow ollama voice text to speech: https://github.com/maudoin/ollama-voice