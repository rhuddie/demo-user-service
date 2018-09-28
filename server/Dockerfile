# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /demo-server

# Copy the current directory contents into the container at /demo-server
COPY . /demo-server

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 80

# Run server.py when the container launches
CMD ["python", "server.py"]
