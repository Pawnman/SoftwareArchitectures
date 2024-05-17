FROM python:3.11
WORKDIR /messenger

COPY ./requirements.txt /messenger/requirements.txt
RUN pip install -r requirements.txt

COPY . /messenger

ENTRYPOINT ["bash", "-c", "cd ./rest-api && uvicorn main:app --port 8080 --host 0.0.0.0"]