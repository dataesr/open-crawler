FROM python:3.11-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/open-crawler

WORKDIR /open-crawler

COPY ./requirements.txt /open-crawler

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/ /open-crawler/app

WORKDIR /open-crawler/app

CMD ["uvicorn", "api.main:api_app", "--host", "0.0.0.0", "--port", "80"]