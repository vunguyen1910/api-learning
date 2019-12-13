from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS
from flask_mail import Mail
import os

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = "super"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

db.init_app(app)
from src.components.cli import create_db
from src.models import Teacher, Course, Recourse, Token, OAuth, Document
app.cli.add_command(create_db)

migrate = Migrate(app, db)

CORS(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return Teacher.query.get(id)
    
mail_setting = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASSWORD')
}

app.config.update(mail_setting)
mail = Mail(app)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

from src.components.teacher import teacher_blueprint
app.register_blueprint(teacher_blueprint, url_prefix="/")

from src.components.oauth import blueprint
app.register_blueprint(blueprint, url_prefix="/loginfacebook")

from src.components.course import course_blueprint
app.register_blueprint(course_blueprint, url_prefix="/course")

from src.components.recourse import recourse_blueprint
app.register_blueprint(recourse_blueprint, url_prefix="/recourse")
