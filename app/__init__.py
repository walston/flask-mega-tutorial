from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# fmt: off # circular import if above `app` declaration
from app import routes
