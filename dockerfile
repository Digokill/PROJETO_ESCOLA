FROM python:3.9-slim

WORKDIR /

COPY /App/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./App .

CMD ["python", "app.py"]