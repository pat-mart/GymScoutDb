"""
This file is a workaround to the circular dependency problems.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from password import get_user, get_pw
from base import Base

cnct_str = f"postgresql+psycopg2://{get_user()}:{get_pw()}@localhost/gymscout"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = cnct_str

db = SQLAlchemy(model_class=Base)

