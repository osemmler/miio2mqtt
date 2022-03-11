FROM python:3.10.2-alpine

WORKDIR /opt/miio2mqtt

COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc libc-dev libffi-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    apk del gcc libc-dev libffi-dev

COPY script script
CMD [ "python3", "script/run.py"]