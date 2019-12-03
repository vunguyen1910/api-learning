from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)
db.init_app(app)
from src.components.cli import create_db
from src.models import Teacher, Course, Recourse
app.cli.add_command(create_db)

migrate = Migrate(app, db)
CORS(app)

login_manager = LoginManager(app)
login_manager.login_view="teachers.login"

from src.components.teacher import teacher_blueprint
app.register_blueprint(teacher_blueprint, url_prefix="/")