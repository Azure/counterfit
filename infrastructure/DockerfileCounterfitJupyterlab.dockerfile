FROM jupyter/minimal-notebook:python-3.8.8

ENV JUPYTER_ENABLE_LAB=yes
USER root
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential git\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i "s/\"default\": \"inherit\"/\"default\": \"dark\"/g" /opt/conda/share/jupyter/lab/schemas/@jupyterlab/terminal-extension/plugin.json
USER 1000
RUN git clone https://github.com/Azure/counterfit.git \
   && cd counterfit \
   && pip install .[dev]\
   && cd ..
EXPOSE 8888
EXPOSE 2718
ENTRYPOINT ["jupyter", "lab", "--ip='0.0.0.0'","--no-browser","--allow-root"] 
