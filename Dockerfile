FROM python:3.11-slim
LABEL authors="vladimirlevin"
LABEL org.opencontainers.image.source=https://github.com/opa-oz/pingwin

WORKDIR /code

EXPOSE 8080

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./server.py /code/server.py

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]