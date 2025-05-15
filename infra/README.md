# Deploying Dify platform

As of today, I found helm charts in the docuementation, yet, the deployment involves storage and a proper CSI with a dynamic volume provisioner, or to setup external to kubernetes cluster postgres, minio, and vector database. This is why I will first start with that docker-compose, and leave for later the work on a kubernetes deployment with external databases.

## Docker Compose based deployment

<https://docs.dify.ai/en/getting-started/install-self-hosted/docker-compose>

target service FQDN : `dify-ai.pesto.io`

```bash
# Assuming current latest version is 0.15.3
export DIFY_RELEASE='1.4.0'
export DIFY_GIT_URI='https://github.com/langgenius/dify.git'
export DEPLOYMENT_HOME="/opt/dify/home"

sudo mkdir -p ${DEPLOYMENT_HOME}
sudo chown pesto:pesto -R /opt/dify

git clone --branch $DIFY_RELEASE --depth=1 $DIFY_GIT_URI ${DEPLOYMENT_HOME}

cd ${DEPLOYMENT_HOME}

cd ./docker

ls -alh ./.env.example

cp .env.example .env
export EXPOSE_NGINX_PORT=9080
export EXPOSE_NGINX_SSL_PORT=9443

sed -i "s#EXPOSE_NGINX_PORT=80#EXPOSE_NGINX_PORT=${EXPOSE_NGINX_PORT}#g" ./.env 
sed -i "s#EXPOSE_NGINX_SSL_PORT=443#EXPOSE_NGINX_SSL_PORT=${EXPOSE_NGINX_SSL_PORT}#g" ./.env 
sed -i "s#CONSOLE_API_URL=#CONSOLE_API_URL=http://api-console-dify-ai.pesto.io#g" ./.env
sed -i "s#CONSOLE_WEB_URL=#CONSOLE_WEB_URL=http://console-dify-ai.pesto.io#g" ./.env
sed -i "s#SERVICE_API_URL=#SERVICE_API_URL=http://api-dify-ai.pesto.io#g" ./.env
sed -i "s#APP_API_URL=#APP_API_URL=http://api-app-dify-ai.pesto.io#g" ./.env
sed -i "s#APP_WEB_URL=#APP_WEB_URL=http://app-dify-ai.pesto.io#g" ./.env
sed -i "s#FILES_URL=#FILES_URL=http://upload-dify-ai.pesto.io#g" ./.env



# ---
# errata
sed -i "s#CONSOLE_API_URL=http://api-console-dify-ai.pesto.io#CONSOLE_API_URL=http://api-console-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env
sed -i "s#CONSOLE_WEB_URL=http://console-dify-ai.pesto.io#CONSOLE_WEB_URL=http://console-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env
sed -i "s#SERVICE_API_URL=http://api-dify-ai.pesto.io#SERVICE_API_URL=http://api-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env
sed -i "s#APP_API_URL=http://api-app-dify-ai.pesto.io#APP_API_URL=http://api-app-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env
sed -i "s#APP_WEB_URL=http://app-dify-ai.pesto.io#APP_WEB_URL=http://app-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env
sed -i "s#FILES_URL=http://upload-dify-ai.pesto.io#FILES_URL=http://upload-dify-ai.pesto.io:${EXPOSE_NGINX_PORT}#g" ./.env



# ---
# Check env customized vars
cat ./.env | grep EXPOSE_NGINX_PORT
cat ./.env | grep EXPOSE_NGINX_SSL_PORT
cat ./.env | grep pesto
docker compose up -d
# it took something like 30 minutes to docker pull all, and start

# ---
# And I could successfully acces it through http://api-console-dify-ai.pesto.io:9080/install

```

I want in `.env`:

```bash


# ------------------------------
# Common Variables
# ------------------------------

# The backend URL of the console API,
# used to concatenate the authorization callback.
# If empty, it is the same domain.
# Example: https://api.console.dify.ai
CONSOLE_API_URL=http://api-console-dify-ai.pesto.io

# The front-end URL of the console web,
# used to concatenate some front-end addresses and for CORS configuration use.
# If empty, it is the same domain.
# Example: https://console.dify.ai
CONSOLE_WEB_URL=http://console-dify-ai.pesto.io

# Service API Url,
# used to display Service API Base Url to the front-end.
# If empty, it is the same domain.
# Example: https://api.dify.ai
SERVICE_API_URL=http://api-dify-ai.pesto.io

# WebApp API backend Url,
# used to declare the back-end URL for the front-end API.
# If empty, it is the same domain.
# Example: https://api.app.dify.ai
APP_API_URL=http://api-app-dify-ai.pesto.io

# WebApp Url,
# used to display WebAPP API Base Url to the front-end.
# If empty, it is the same domain.
# Example: https://app.dify.ai
APP_WEB_URL=http://app-dify-ai.pesto.io

# File preview or download Url prefix.
# used to display File preview or download Url to the front-end or as Multi-model inputs;
# Url is signed and has expiration time.
# Setting FILES_URL is required for file processing plugins.
#   - For https://example.com, use FILES_URL=https://example.com
#   - For http://example.com, use FILES_URL=http://example.com
#   Recommendation: use a dedicated domain (e.g., https://upload.example.com).
#   Alternatively, use http://<your-ip>:5001 or http://api:5001,
#   ensuring port 5001 is externally accessible (see docker-compose.yaml).
FILES_URL=http://upload-dify-ai.pesto.io

####
# And also

export EXPOSE_NGINX_PORT=80
export EXPOSE_NGINX_SSL_PORT=443

```



So for the `/etc/hosts`:

```bash

export OPS_HOME=$(mktemp -d CONF_DIFY_AI_ETC_HOSTS_XXXXX)
export DEPLOYED_SERVICE_IPADDR='192.168.1.13'

cat <<EOF >${OPS_HOME}/dify.etc.hosts.addon
# ---
# Dify AI services
${DEPLOYED_SERVICE_IPADDR}    api-console-dify-ai.pesto.io
${DEPLOYED_SERVICE_IPADDR}    console-dify-ai.pesto.io
${DEPLOYED_SERVICE_IPADDR}    api-dify-ai.pesto.io
${DEPLOYED_SERVICE_IPADDR}    api-app-dify-ai.pesto.io
${DEPLOYED_SERVICE_IPADDR}    app-dify-ai.pesto.io
${DEPLOYED_SERVICE_IPADDR}    upload-dify-ai.pesto.io
EOF

cat ${OPS_HOME}/dify.etc.hosts.addon

# ---
# UNIX
cat ${OPS_HOME}/dify.etc.hosts.addon | sudo tee -a /etc/hosts
ping -c 4 api-console-dify-ai.pesto.io

# --- 
# Git bash for WINDOWS executed as admin

cat ${OPS_HOME}/dify.etc.hosts.addon | tee -a /c/Windows/System32/drivers/etc/hosts
ping api-console-dify-ai.pesto.io

rm ${OPS_HOME}/dify.etc.hosts.addon
```


Ok so when my dify works, my issue is that I need a voice to text AI service, and all of them online are like non free (which we understand)

SO I will try and setup a simple Speech to text onpremise, apparently OLLAMA would allow installing a whisper model, we'll see how good it is:

https://www.arsturn.com/blog/using-ollama-for-automated-voice-transcription


## Kubernetes Helm Chart

* <https://github.com/douban/charts/tree/master/charts/dify>

I need there:

* an external postgres
* an external minio
* an external vector db:
  * <https://github.com/mileszim/awesome-vector-database?tab=readme-ov-file#open-source-databases>
  * so i need to choose `milvus` as suggested by <https://github.com/douban/charts/tree/master/charts/dify#setup-vector-db>
  * <https://milvus.io/docs/install-overview.md>
  * docker standalone will be enough up to 100 millions vectors <https://milvus.io/docs/install_standalone-docker.md>
  * you will need milvus distributed in a kubernetes cluster for more than a hundred million vectors, up to tens of billions of vectors (there's a kubernetes operator, i will need the topolvm CSI with its dynamic volume provisioner lvmd on each cluster node): <https://milvus.io/docs/install_cluster-milvusoperator.md>
  * note i found in the docker-compose env example file, the possible supported vector db. Supported DBs are:
    * `weaviate`,
    * `qdrant`,
    * `milvus`,
    * `myscale`,
    * `relyt`,
    * `pgvector`,
    * `pgvecto-rs`,
    * `chroma`,
    * `opensearch`,
    * `oracle`,
    * `tencent`,
    * `elasticsearch`,
    * `elasticsearch-ja`,
    * `analyticdb`,
    * `couchbase`,
    * `vikingdb`,
    * `oceanbase`,
    * `opengauss`,
    * `tablestore`,
    * `vastbase`,
    * `tidb`,
    * `tidb_on_qdrant`,
    * `baidu`,
    * `lindorm`,
    * `huawei_cloud`,
    * `upstash`
    * config param in env config file is `VECTOR_STORE=weaviate`
