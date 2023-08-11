# Use an official Node.js runtime as the parent image
FROM node

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install the Wappalyzer CLI tool globally
SHELL ["/bin/bash", "-c"]

# Update and install necessary utilities
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    libxss1

# Install Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get install -y ./chrome.deb && \
    rm ./chrome.deb

WORKDIR /app

COPY ./requirements.txt /app

ENV PYTHON_VENV=/opt/venv
RUN python3 -m venv $PYTHON_VENV
ENV PATH="$PYTHON_VENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./open_crawler/ /app

## Set CHROME_PATH environment variable
ENV CHROME_PATH=/usr/bin/google-chrome

WORKDIR /

# Clone the Wappalyzer repository
RUN git clone https://github.com/wappalyzer/wappalyzer.git

## Move into the wappalyzer directory
WORKDIR /wappalyzer

# Install dependencies using yarn and link it
RUN yarn install && yarn run link

WORKDIR /app

# Specify the command to run on container start (for this example, it's just a shell)
CMD [ "bash" ]
