FROM python:3.10-alpine
WORKDIR /watch

RUN apk add --update --no-cache ffmpeg imagemagick

ADD requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD webwatcher /app/webwatcher

VOLUME /watch
VOLUME /source

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"
ENV IS_DOCKER=true

ENTRYPOINT ["python", "-m", "webwatcher"]


