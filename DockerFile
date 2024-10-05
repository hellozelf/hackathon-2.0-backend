FROM python:3.12.2-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev musl-dev build-essential

COPY requirements.txt requirements.txt

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN  pip install pip --upgrade && \
     pip install -r requirements.txt

COPY . .
