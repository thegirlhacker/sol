FROM python:3.13.1-slim
COPY runtime.sh /tmp/runtime.sh
RUN sh /tmp/runtime.sh && rm /tmp/runtime.sh
RUN useradd --create-home --shell /bin/bash --uid 1000 agent
COPY builder   /app/builder
COPY docs      /app/docs
COPY wheelhouse /app/wheelhouse
COPY vendor    /app/vendor
COPY build     /app/build
COPY tests     /app/tests
COPY build.json requirements.lock /app/
ENV PYTHONPATH=/app
WORKDIR /app
RUN mkdir -p /app/out && chown -R agent:agent /app
USER agent
