# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_babel import Babel

#Instantiate opjects 
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin(template_mode='bootstrap4')
babel = Babel()