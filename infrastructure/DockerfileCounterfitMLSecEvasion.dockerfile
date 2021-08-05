# azuretrustworthyml/counterfit-mlsecevasion
FROM jupyter/base-notebook:python-3.8.8

ENV JUPYTER_ENABLE_LAB=yes
WORKDIR /home/jovyan
USER root
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential git upx-ucl\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i "s/\"default\": \"inherit\"/\"default\": \"dark\"/g" /opt/conda/share/jupyter/lab/schemas/@jupyterlab/terminal-extension/plugin.json
USER 1000
RUN git clone --single-branch --branch mlsecevasion/2021 https://github.com/Azure/counterfit.git \
   && cd counterfit \
   && pip install --no-cache-dir -r requirements.txt \
   && python -c 'import ssl, nltk; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download("stopwords")' \
   && cd .. \
   && echo "cd counterfit && python counterfit.py" > /home/jovyan/.bash_profile

EXPOSE 8888