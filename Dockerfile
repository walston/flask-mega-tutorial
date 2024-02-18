FROM python:3.12-slim-bookworm
WORKDIR /usr/src
COPY ./requirements.txt /usr/src
RUN ["pip", "install", "-r", "requirements.txt"]
ENV FLASK_APP=microblog.py
EXPOSE 8080
CMD ["flask", "--app", "run", "--host", "0.0.0.0", "--port", "8080"]