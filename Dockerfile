FROM ubuntu:20.04

EXPOSE 8000

RUN apt-get update && apt install -y --no-install-recommends ffmpeg python3-pip python3-venv

ADD . /PDMAutoSession

WORKDIR /PDMAutoSession

RUN pip install -r requirements.txt

RUN python3 manage.py makemigrations

RUN python3 manage.py migrate

Run python3 manage.py loaddata data1.json

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]