FROM python:3.9-slim

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Python logs to STDOUT
    PYTHONUNBUFFERED=1

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY requirements.txt /tmp/

RUN set -x buildDeps=" \
    build-essential \
    " \
    && runDeps="" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps $runDeps \
    # Install Python dependencies
    && pip install -r /tmp/requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app

ADD . /app

WORKDIR /app/app

CMD sleep infinity
