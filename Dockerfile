FROM python:3.12-slim-bookworm
WORKDIR /usr/src
COPY ./requirements.txt /usr/src
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["flask", "--app", "src/hello.py", "--debug", "run"]