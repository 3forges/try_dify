# The NextJS Standalone App

## Run it

```bash
cd ./app/template

pnpm i

export NEXT_PUBLIC_APP_KEY='app-3p53qo1rj1zUw8KlGTrcXUPM'
export NEXT_PUBLIC_APP_ID='https://udify.app/chat/8617tIdhiJs5HLXI'
export NEXT_PUBLIC_APP_ID='8617tIdhiJs5HLXI'
export NEXT_PUBLIC_API_URL=''
export NEXT_PUBLIC_API_URL='https://api.dify.ai/v1'
export NEXT_PUBLIC_APP_TYPE_WORKFLOW='false'
export NODE_TLS_REJECT_UNAUTHORIZED=0

pnpm dev

```

### Speech to text

Now with that app, my problem is that I want to undertand how to use the dify ai api for speech to text features. 

I found this:

* https://github.com/langgenius/dify/discussions/4824


Ok there I found a very simple python code to turn speech into text:

```Python
import requests
from yarl import URL

class LocalAISpeech2text:
    def __init__(self, server_url):
        self.server_url = server_url

    def transcribe_audio(self, model: str, audio_file_path: str) -> str:
        url = str(URL(self.server_url) / "v1/audio/transcriptions")
        data = {"model": model}
        files = {"file": open(audio_file_path, 'rb')}

        response = requests.post(url, data=data, files=files)
        response.raise_for_status()

        if 'error' in response.json():
            raise Exception("Error in transcription: " + response.json()['error'])

        return response.json()["text"]

# Example usage
stt = LocalAISpeech2text(server_url="http://localhost:5000")
transcription = stt.transcribe_audio(model="whisper", audio_file_path="path/to/audio/file.wav")
print(transcription)
```

So now I will have to find out how to turn that into typescript

My only question is there: what is YARL in URL python package?

* in `files = {"file": open(audio_file_path, 'rb')}` , the `rb` means _read binary_.
* 



## Run with Docker

```bash
docker build -t tolt/whisper:0.0.1 .
```

```bash
docker run --name VoyageVocab \
  --restart unless-stopped \
  -itd -p 0.0.0.0:7860:7860 \
  tolt/whisper:0.0.1

# docker stop VoyageVocab && docker rm VoyageVocab

# ---
# Then I waited laong time that the app starts, because
# python dependencies installations were run in the
# startup command

docker commit VoyageVocab tolt/whisper:0.0.2

# And then I ran:

docker stop VoyageVocab && docker rm VoyageVocab

docker run --name VoyageVocab \
  --restart unless-stopped \
  -itd -p 0.0.0.0:7860:7860 \
  tolt/whisper:0.0.2

docker exec -u root VoyageVocab bash -c 'rm /tolt/app/VoyageVocab.py'
docker cp ./VoyageVocab.py VoyageVocab:/tolt/app/
docker exec -u root VoyageVocab bash -c 'chown tolt:tolteques -R /tolt/app/'

docker exec -u root VoyageVocab bash -c 'ls -alh /tolt/app/'

docker restart VoyageVocab

docker logs -f VoyageVocab


```


## Whisper on Kubernetes

I found:

* https://artifacthub.io/packages/helm/test-opea/whisper