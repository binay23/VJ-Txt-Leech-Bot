FROM python:3.10.8-slim-buster

# Update system, install dependencies including ffmpeg, aria2, gcc, and libraries
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev ffmpeg aria2 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application files into the container
COPY . /app/
WORKDIR /app/

# Install required Python dependencies
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Start the bot application (main.py)
CMD python3 main.py
