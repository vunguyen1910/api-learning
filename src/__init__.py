from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

from src.models.course import Course
from src.models.recourse import Recourse
from src.models.student import Student, StudentCourse
from src.models.teacher import Teacher

migrate = Migrate(app, db)

db.create_all()

@app.route('/')
def root():
    return "OKE"