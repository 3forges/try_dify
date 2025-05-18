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

# Those two below freaking work after i pulled the model

# -
# the default is streaming, so i will need to use RxJs and perhaps websockets we'll see

export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "Eomer/gpt-3.5-turbo", "prompt": "What is water made of?" }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate


export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "Eomer/gpt-3.5-turbo", "prompt": "What is water made of?", "stream": false }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate


```

Example working output for a curl on `gpt-3.5-turbo`:

```bash
$ export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "Eomer/gpt-3.5-turbo", "prompt": "What is water made of?", "stream": false }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate
Note: Unnecessary use of -X or --request, POST is already inferred.
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 192.168.1.13:11434...
* Connected to 192.168.1.13 (192.168.1.13) port 11434
> POST /api/generate HTTP/1.1
> Host: 192.168.1.13:11434
> User-Agent: curl/8.8.0
> Accept: */*
> Content-Length: 87
> Content-Type: application/x-www-form-urlencoded
>
} [87 bytes data]
* upload completely sent off: 87 bytes
100    87    0     0  100    87      0      2  0:00:43  0:00:38  0:00:05     0< HTTP/1.1 200 OK
< Content-Type: application/json; charset=utf-8
< Date: Fri, 16 May 2025 09:26:43 GMT
< Content-Length: 1667
<
{ [1667 bytes data]
100  1754  100  1667  100    87     41      2  0:00:43  0:00:39  0:00:04   418HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Date: Fri, 16 May 2025 09:26:43 GMT
Content-Length: 1667

{"model":"Eomer/gpt-3.5-turbo","created_at":"2025-05-16T09:26:42.97400598Z","response":"Ah, an excellent question! Water is made up of two hydrogen atoms and one oxygen atom, which are held together by strong ionic bonds. The chemical formula for water is H2O. Isn't that fascinating? 💧\n\nBut wait, there's more! Water also contains trace amounts of other elements like sodium, potassium, and calcium, which can affect its taste and properties. And did you know that water can exist in three different states: liquid, solid (ice), and gas (water vapor)? 😮\n\nSo, what would you like to know next about water? 🤔","done":true,"done_reason":"stop","context":[518,25580,29962,3532,14816,29903,6778,3492,526,263,19780,20255,19423,829,14816,29903,6778,13,13,5618,338,4094,1754,310,29973,518,29914,25580,29962,13,17565,29892,385,15129,1139,29991,13062,338,1754,701,310,1023,17546,1885,28422,322,697,288,28596,12301,29892,607,526,4934,4208,491,4549,16346,293,289,13788,29889,450,22233,7063,363,4094,338,379,29906,29949,29889,29489,29915,29873,393,21028,262,1218,29973,29871,243,162,149,170,13,13,6246,4480,29892,727,29915,29879,901,29991,13062,884,3743,9637,26999,310,916,3161,763,20892,1974,29892,3104,465,1974,29892,322,15835,398,29892,607,508,6602,967,21779,322,4426,29889,1126,1258,366,1073,393,4094,508,1863,297,2211,1422,5922,29901,23904,29892,7773,313,625,511,322,10489,313,13405,325,26191,6877,29871,243,162,155,177,13,13,6295,29892,825,723,366,763,304,1073,2446,1048,4094,29973,29871,243,162,167,151],"total_duration":39859847349,"load_duration":16397622,"prompt_eval_count":31,"prompt_eval_duration":267383118,"eval_count":144,"eval_duration":39575360365}
* Connection #0 to host 192.168.1.13 left intact

```


I also found a possible issue about the whipser model i have pulled:

```bash
pesto@pesto:/opt/dify/home/docker$ docker exec -it pesto-ollama bash -c 'ollama show dimavz/whisper-tiny'
  Model
panic: interface conversion: interface {} is nil, not string

goroutine 1 [running]:
github.com/ollama/ollama/cmd.showInfo.func2()
        github.com/ollama/ollama/cmd/cmd.go:687 +0x8c5
github.com/ollama/ollama/cmd.showInfo.func1({0x55edc160a1ca, 0x5}, 0xc000587bc8)
        github.com/ollama/ollama/cmd/cmd.go:680 +0x182
github.com/ollama/ollama/cmd.showInfo(0xc0006403c0, 0x0, {0x55edc1aacd18?, 0xc00011c038?})
        github.com/ollama/ollama/cmd/cmd.go:685 +0x86
github.com/ollama/ollama/cmd.ShowHandler(0xc000201808, {0xc000468f20, 0x1, 0x55edc1609072?})
        github.com/ollama/ollama/cmd/cmd.go:663 +0x78c
github.com/spf13/cobra.(*Command).execute(0xc000201808, {0xc000468ee0, 0x1, 0x1})
        github.com/spf13/cobra@v1.7.0/command.go:940 +0x85c
github.com/spf13/cobra.(*Command).ExecuteC(0xc000201208)
        github.com/spf13/cobra@v1.7.0/command.go:1068 +0x3a5
github.com/spf13/cobra.(*Command).Execute(...)
        github.com/spf13/cobra@v1.7.0/command.go:992
github.com/spf13/cobra.(*Command).ExecuteContext(...)
        github.com/spf13/cobra@v1.7.0/command.go:985
main.main()
        github.com/ollama/ollama/main.go:12 +0x4d
pesto@pesto:/opt/dify/home/docker$ docker exec -it pesto-ollama bash -c 'ollama show Eomer/gpt-3.5-turbo'
  Model
    architecture        llama
    parameters          6.7B
    context length      4096
    embedding length    4096
    quantization        Q4_0

  Capabilities
    completion

  Parameters
    stop    "[INST]"
    stop    "[/INST]"
    stop    "<<SYS>>"
    stop    "<</SYS>>"

  System
    You are a friendly assistant.

  License
    LLAMA 2 COMMUNITY LICENSE AGREEMENT
    Llama 2 Version Release Date: July 18, 2023


```

```bash
# ---
# msitral also works, but is muuuch slower than GPT-3.5 turbo
export OLLAMA_SERVICE_IPADDR="192.168.1.13"
curl -X POST -d '{ "model": "mistral:7b", "prompt": "What is water made of?", "stream": false }' -ivvv http://${OLLAMA_SERVICE_IPADDR}:11434/api/generate

```

for chat in typescript awesome: https://www.youtube.com/watch?app=desktop&v=QUJHEvCqhdw


MAYBE THIS CODE WILL WORK FOR SPEECH TO TEXT: https://github.com/maudoin/ollama-voice

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

also i'd say even more hope on https://github.com/didevlab/audio-transcriber-whisper-api (but that one i really don't know if it can itnterate in dify)


## OLLAMA SPEECH TO TEXT EXAMPLES

* one:
  * https://dev.to/dartisan/how-i-built-a-local-voice-enabled-ai-chatbot-with-langchain-and-ollama-dap
  * https://github.com/D-artisan/ai-chatbot

* two in react:
  * https://dev.to/emojiiii/how-to-build-a-speech-to-text-app-with-react-and-transformersjs-4n1f

* better innodejs:
  * https://dev.to/aswinvijayano/building-a-real-time-voice-assistant-with-local-llms-on-a-raspberry-pi-4inh
  * it relies on mitral: so i can modify it to use speech to  text on mistral model like https://github.com/D-artisan/ai-chatbot


### try D-artisan 's ai-chatbot


```bash
git clone https://github.com/D-artisan/ai-chatbot
cd ai-chatbot

export OCI_IMG='python:3.12-slim-bookworm'

docker run --name ai_chatbot -itd \
  --restart unless-stopped \
  -v $PWD:/opt/ai_chatbot:rw \
  ${OCI_IMG} \
  bash

docker exec -w /opt/ai_chatbot -it ai_chatbot bash -c 'pwd && id && ls -alh && pip install -r requirements.txt'
# ok too bad, it requrires running on windows:
# ERROR: Could not find a version that satisfies the requirement pywin32==310 (from versions: none)


### docker exec -w /opt/ai_chatbot -it ai_chatbot bash -c 'pwd && id && ls -alh && streamlit run UIChat.py'

```


#### On windowds i could connect to my private server:

```bash


python -m pip install -r requirements.txt

mkdir -p ~/.streamlit/

cat <<EOF >./streamlit.config.toml
[browser]
serverAddress = '0.0.0.0'
EOF

cat config | tee -a ~/.streamlit/config.toml

python -m streamlit run UIChat.py

```

Aller, j'ai découvert le poteau rose, cette app de merde utilise l'API google pour l Speech to text, il y a ça dans le code:

```Python
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.warning("Could not understand audio")
    except sr.RequestError as e:
        st.error(f"Speech recognition error: {e}")
    return ""
```

je peux pull gpt-35 turbo comme celui qui a marché sur dify:

```bash
docker exec -it pesto-ollama bash -c 'ollama pull Eomer/gpt-3.5-turbo'

docker exec -it pesto-ollama bash -c 'ollama run Eomer/gpt-3.5-turbo'

# et je refait mon test 
cd ~/quicktests_whisper
ls -alh ./test/harvard.wav

curl --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="Eomer%2Fgpt-3.5-turbo"' http://192.168.1.13:11434/api/chat

curl --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="Eomer/gpt-3.5-turbo"' http://192.168.1.13:11434/api/chat


curl --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="Eomer%2Fgpt-3.5-turbo"' http://192.168.1.13:11434/api/generate

curl --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="Eomer/gpt-3.5-turbo"' http://192.168.1.13:11434/api/generate



curl -H 'Content-Type: audio/mpeg' --expect100-timeout 360000 -X POST -ivvv -F 'file=@"./test/harvard.wav"' -F 'model="Eomer/gpt-3.5-turbo"' http://192.168.1.13:11434/api/chat



```

And i foud a guy looking for the same than me: https://discuss.huggingface.co/t/how-to-use-tts-stt-with-mistral-7b-or-other-llms-for-an-offline-voice-assistant/61155/2

but this does nto give an example relying on compelte offline, its all relying on openai

Now I found https://github.com/camenduru/voice-chat-with-mistral-hf/blob/main/app.py , which relies on whisper, but then not easy to say how to adapt it to ollama

and i am back to https://www.arsturn.com/blog/using-ollama-for-automated-voice-transcription

and I found https://github.com/OlgaSeleznova/VoyageVocab/tree/main

### Try https://github.com/OlgaSeleznova/VoyageVocab/tree/main

related post : https://medium.com/@olgaselesnyova/exploring-ai-a-step-by-step-project-using-ollama-whisper-and-gradio-223f9a1300f8

```bash

git clone https://github.com/OlgaSeleznova/VoyageVocab

cd VoyageVocab



python -m pip install langchain langchain-community gradio git+https://github.com/openai/whisper.git

# and I think this one will need to be executed inside the ollama docker container directly, where the mistrla model is installed and running.

# docker exec -it pesto-ollama bash -c 'ollama pull Eomer/gpt-3.5-turbo'
# docker commit pesto-ollama pesto.io/pesto/ollama-with-models:gpt-3.5-turbo
# pesto-ollama pesto.io/pesto/ollama-with-models:gpt-3.5-turbo

```

Omy i found this: https://github.com/ollama-interface/Ollama-Gui?tab=readme-ov-file

## OLLAMA API REFERENCE

I found it here: https://github.com/ollama/ollama/blob/main/docs/api.md?plain=1


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