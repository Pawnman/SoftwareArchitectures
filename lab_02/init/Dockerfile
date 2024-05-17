FROM python:3.11
WORKDIR /init

COPY ./requirements.txt /init/requirements.txt
RUN pip install -r requirements.txt

COPY . /init

ENTRYPOINT ["bash", "-c", "python3 upload_script.py"]