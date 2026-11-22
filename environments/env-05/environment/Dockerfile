FROM python:3.13.1-slim
COPY runtime.sh /tmp/runtime.sh
RUN sh /tmp/runtime.sh && rm /tmp/runtime.sh
RUN useradd --create-home --shell /bin/bash --uid 1000 agent
COPY taskr /app/taskr
COPY docs  /app/docs
COPY data  /app/data
COPY tests /app/tests
COPY config.json /app/
ENV PYTHONPATH=/app
WORKDIR /app
RUN mkdir -p /app/var && chown -R agent:agent /app
USER agent
