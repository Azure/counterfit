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
COPY . .

RUN pip install .[dev]
EXPOSE 8888