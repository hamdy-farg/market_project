from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'd24151e7ccc11a9bcf3e57d96b7523ee'
app.app_context().push()
db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager  = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from market import routes