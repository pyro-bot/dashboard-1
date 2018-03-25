from flask import Flask
from flask_admin import  Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import dash

app = Flask(__name__)
admin = Admin(app)
dash = dash.Dash(__name__, server=app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Brik:89505@localhost:3306/teplo'
app.secret_key = 'asdasdadadadadadasdads'
db = SQLAlchemy(app)
conn = db.engine

from board import models, admin_panel, dashboard

migrate = Migrate(app, db)


