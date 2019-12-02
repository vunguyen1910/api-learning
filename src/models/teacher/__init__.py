from flask_login import UserMixin
from src import db

class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(255), unique = True, nullable = False)
    phone = db.Column(db.Integer, unique= True, nullable = False )
    course_id = db.relationship('Course', backref='teacher', lazy = True)
    recourse_id = db.relationship('Recourse', backref='teacher', lazy = True)