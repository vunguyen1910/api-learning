from src import db
from flask_login import UserMixin


class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(255), nullable = False)
    phone = db.Column(db.Integer, unique= True, nullable = False)
    registered_course = db.relationship('Course', secondary = "StudentCourse", lazy='subquery', backref = db.backref('students', lazy = True))

class StudentCourse(db.Model):
    __tablename__ = 'studentcourse'
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))