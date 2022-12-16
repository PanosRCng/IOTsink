FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt


RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app


ENV MODULE_NAME="iotsink.iotsink"

ENV MAX_WORKERS=1

ENV PORT=8080
ENV TIMEOUT="1200"
ENV KEEP_ALIVE="1200"
ENV GRACEFUL_TIMEOUT="1400"
ENV LOG_LEVEL="debug"

EXPOSE 8080