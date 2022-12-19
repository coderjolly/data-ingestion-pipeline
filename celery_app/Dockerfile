FROM python:alpine3.17

COPY celery_app /usr/src/celery_app/
COPY db_clients /usr/src/db_clients
COPY worker_tasks /usr/src/worker_tasks/

RUN apk add --no-cache python3 py3-pip bash
RUN pip install --upgrade pip

RUN cd /usr/src/celery_app && ls
RUN cd /usr/src/db_clients && ls
RUN cd /usr/src/worker_tasks && ls

RUN pip install -r /usr/src/celery_app/requirements.txt
RUN pip install /usr/src/db_clients
RUN pip install /usr/src/worker_tasks

ENTRYPOINT python3 /usr/src/celery_app/main.py \
    --concurrency 2 \
    -Q steam_data_processor \
    --loglevel INFO
