from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
db = SQLAlchemy(app)