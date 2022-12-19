FROM python:alpine3.17

COPY async_backend /usr/src/async_backend/
COPY db_clients /usr/src/db_clients
COPY worker_tasks /usr/src/worker_tasks/

RUN apk add --no-cache python3 py3-pip bash
RUN pip install --upgrade pip

RUN cd /usr/src/async_backend && ls
RUN cd /usr/src/db_clients && ls
RUN cd /usr/src/worker_tasks && ls

RUN pip install -r /usr/src/async_backend/requirements.txt
RUN pip install /usr/src/db_clients/
RUN pip install /usr/src/worker_tasks/

WORKDIR /usr/src/async_backend

EXPOSE 5000

CMD ["python3", "main.py"]
