# Use an official Python runtmie as a parent image
FROM --platform=linux/amd64 python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in the requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run get_tweets.py when the container launches
CMD ["python", "get_tweets.py"]
