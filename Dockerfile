# Use an official Python runtime as a parent image
FROM python:3.7

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./Asclepius.png ./Asclepius.png
COPY ./README.md ./README.md
COPY ./config.py ./config.py
COPY ./main.py ./main.py
COPY ./config.env ./config.env
COPY ./repository ./repository
COPY ./util ./util
COPY ./requirements.txt ./requirements.txt


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "-m", "main.py"]

