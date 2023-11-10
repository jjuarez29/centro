FROM python:3.13.0a1-alpine3.18

WORKDIR /app

COPY . /app

#RUN pip install --no-cache-dir Flask pymongo
RUN pip install --no-cache-dir Flask pymongo redis
#EXpose 5001  error mando
EXPOSE 5002

CMD ["python", "main.py"]
