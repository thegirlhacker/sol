FROM python:3.13.1-slim
COPY runtime.sh /tmp/runtime.sh
RUN sh /tmp/runtime.sh && rm /tmp/runtime.sh
COPY . /tests
RUN useradd --no-create-home --uid 1001 runner
