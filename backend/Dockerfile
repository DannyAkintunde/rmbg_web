FROM python:3.7.15-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apk update

COPY ./backend/requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM python:3.7.15-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local

COPY ./backend .

EXPOSE 8000

ENTRYPOINT ["python3", "-u", "app.py"]
