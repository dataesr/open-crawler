FROM python:3.11-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./open_crawler/ /app

CMD ["uvicorn", "api.main:api_app", "--host", "0.0.0.0", "--port", "80"]