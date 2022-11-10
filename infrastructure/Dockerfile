FROM python:3.8.9-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash counterfituser

WORKDIR /home/counterfituser

COPY . .

RUN pip install .[dev]

RUN chown -R counterfituser:counterfituser /home/counterfituser
USER counterfituser

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION python

CMD ["/bin/bash"]