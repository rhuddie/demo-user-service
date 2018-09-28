# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /demo-server

# Copy the current directory contents into the container at /demo-server
COPY . /demo-server

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN rm -rf /var/lib/apt/lists/*
RUN apt-get -y update && \
    apt-get install -y gnupg wget

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y \
        xvfb \
        google-chrome-stable \
        chromedriver

# Make port 5000 available to the world outside this container
EXPOSE 80

# Run server.py when the container launches
CMD ["python", "server/server.py"]
