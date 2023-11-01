from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qatamatab@localhost/Kino'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
adm_pwd = generate_password_hash('default')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
from app.models import *

db.create_all()








