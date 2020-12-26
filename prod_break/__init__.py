from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "7be87f5097974366dfe642c7f0c0b608"  # from built-in secrets module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # database path

db = SQLAlchemy(app)  # instance of SQLAlchemy database

from prod_break import routes