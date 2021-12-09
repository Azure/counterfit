FROM python:3.8.9-slim-buster

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends build-essential\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash counterfituser

WORKDIR /home/counterfituser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install tensorflow python-Levenshtein


COPY . .

RUN chown -R counterfituser:counterfituser /home/counterfituser
USER counterfituser

CMD ["/bin/bash"]