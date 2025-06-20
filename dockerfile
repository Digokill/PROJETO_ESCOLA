FROM python:3.9-slim

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./App .
COPY ./logging_config.py logging_config.py

CMD ["python", "app.py"]