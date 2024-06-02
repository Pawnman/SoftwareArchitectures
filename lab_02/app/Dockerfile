FROM python:3.11
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["bash", "-c", "cd ./rest-api && uvicorn main:app --port 8080 --host 0.0.0.0"]