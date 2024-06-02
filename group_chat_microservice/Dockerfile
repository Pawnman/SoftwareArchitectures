FROM python:3.11

WORKDIR /group_chat_service

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
