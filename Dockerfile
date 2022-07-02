FROM python:3.10.5-alpine3.16

RUN adduser -D python

WORKDIR /home/python/app

COPY . .

USER python

RUN pip install --disable-pip-version-check -r requirements.txt

CMD ["python", "./main.py"]