FROM node

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

SHELL ["/bin/bash", "-c"]

# Update and install necessary utilities
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv

# Install Google Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get install -y ./chrome.deb && \
    rm ./chrome.deb

# Install Lighthouse globally
RUN npm install -g lighthouse

# Set CHROME_PATH environment variable
ENV CHROME_PATH=/usr/bin/google-chrome

WORKDIR /app

COPY ./requirements.txt /app

ENV PYTHON_VENV=/opt/venv
RUN python3 -m venv $PYTHON_VENV
ENV PATH="$PYTHON_VENV/bin:$PATH"

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./open_crawler/ /app

CMD ["uvicorn", "api.main:api_app", "--host", "0.0.0.0", "--port", "80"]