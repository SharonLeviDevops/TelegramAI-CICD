FROM python:3.8.12-slim-buster
WORKDIR /app
COPY config-dev.json config-prod.json /app/
COPY . .
RUN pip install -r worker/requirements.txt


CMD ["python3", "-m", "worker.app"]