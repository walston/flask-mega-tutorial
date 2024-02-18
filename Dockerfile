FROM python:3.12-slim-bookworm
WORKDIR /usr/src
COPY ./requirements.txt /usr/src
ENV FLASK_APP="/usr/src/microblog.py"
ENV SQLALCHEMY_DATABASE_URI="/usr/src/app.db"
RUN ["pip", "install", "-r", "requirements.txt"]
EXPOSE 8080
CMD ["flask", "--app", "run", "--host", "0.0.0.0", "--port", "8080"]