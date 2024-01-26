# syntax=docker/dockerfile:1

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY ./src /src
WORKDIR /

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "2900"]
