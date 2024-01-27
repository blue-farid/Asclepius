FROM python:3.7

WORKDIR /app

# Copying files
COPY ./requirements.txt ./requirements.txt
COPY ./Asclepius.png ./Asclepius.png
COPY ./README.md ./README.md
COPY ./config.py ./config.py
COPY ./main.py ./main.py
COPY ./.env ./.env
COPY ./repository ./repository
COPY ./util ./util

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Run the application
CMD ["python3", "main.py"]

