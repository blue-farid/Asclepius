FROM python:3.7 as builder

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

FROM alpine:latest

WORKDIR /app

COPY ./Asclepius.png ./Asclepius.png
COPY ./README.md ./README.md
COPY ./config.py ./config.py
COPY ./main.py ./main.py
COPY ./config.env ./config.env
COPY ./repository ./repository
COPY ./util ./util
COPY --from=builder /app /app

RUN apk add --update python3 py3-pip

EXPOSE 8080

CMD ["python", "-m", "main.py"]
