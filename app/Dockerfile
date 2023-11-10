FROM python:3.13.0a1-alpine3.18

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install redis


COPY . .

CMD ["python", "app.py"]
