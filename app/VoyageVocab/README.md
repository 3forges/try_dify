# The whisper image

```bash
export OCI_IMG='bitnami/python:3.13.3-debian-12-r13'
export CONTAINER_NAME='whisperpeak'

docker run --name ${CONTAINER_NAME} \
  -itd ${OCI_IMG} bash

docker exec -it ${CONTAINER_NAME} bash -c 'python --version'

```

```bash
docker build -t tolt/whisper:0.0.1 .

docker run --name VoyageVocab \
  --restart unless-stopped \
  -itd -p 0.0.0.0:7860:7860 \
  tolt/whisper:0.0.1
```
