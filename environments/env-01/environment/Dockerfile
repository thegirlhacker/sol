FROM python:3.13.1-slim

COPY runtime.sh /tmp/runtime.sh
RUN sh /tmp/runtime.sh && rm /tmp/runtime.sh

# The agent works unprivileged.
RUN useradd --create-home --shell /bin/bash --uid 1000 agent

COPY sync   /app/sync
COPY ingest /app/ingest
COPY docs   /app/docs
COPY data   /app/data
COPY tests  /app/tests
COPY config.json /app/config.json

ENV PYTHONPATH=/app
WORKDIR /app
RUN mkdir -p /app/var && chown -R agent:agent /app
USER agent
