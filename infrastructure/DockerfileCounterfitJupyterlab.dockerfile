FROM jupyter/base-notebook:python-3.8.8

ENV JUPYTER_ENABLE_LAB=yes
WORKDIR /home/jovyan
USER root
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential git\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i "s/\"default\": \"inherit\"/\"default\": \"dark\"/g" /opt/conda/share/jupyter/lab/schemas/@jupyterlab/terminal-extension/plugin.json
USER 1000
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install tensorflow rapidfuzz
RUN git clone https://github.com/Azure/counterfit.git \
   && cd counterfit \
   && python -c 'import ssl, nltk; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download("stopwords")' \
   && cd .. \
   && echo "cd counterfit && python counterfit.py" > /home/jovyan/.bash_profile \
   && mkdir counterfit/counterfit/targets/satelliteimages/results \
   && ln -s counterfit/counterfit/targets/satelliteimages/results satelliteimages \
   && ln -s counterfit/demo/WEBINAR-DEMO-?.md .

EXPOSE 8888