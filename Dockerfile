FROM python:3.12-slim-bookworm
WORKDIR /usr/src
COPY . /usr/src

COPY ./requirements.txt /usr/src
RUN ["pip", "install", "-r", "requirements.txt"]
ENV FLASK_APP="/usr/src/microblog.py"
ENV SQLALCHEMY_DATABASE_URI="/usr/src/app.db"
ENV FLASK_PORT="5000"
EXPOSE 5000
CMD ["flask", "run"]