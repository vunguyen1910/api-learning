from flask_login import UserMixin
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text)
    email = db.Column(db.String(255), unique = True)
    phone = db.Column(db.Integer, unique= True)
    course_id = db.relationship('Course', backref='teacher', lazy = True)
    recourse_id = db.relationship('Recourse', backref='teacher', lazy = True)
    password = db.Column(db.String(120))
    score = db.Column(db.Integer)
    recomments = db.relationship('Recomment', backref="teacher", lazy = True)

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return Teacher.query.filter_by(email=self.email).first()
    def get_teacher(self):
        return{
            "id" : self.id,
            "name": self.name,
            "desc": self.desc,
            "avata_url": self.avata_url,
            "email": self.email,
            "phone": self.phone,
            "score": self.score
        }

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=False)
    user = db.relationship(Teacher)

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable = False)
    user = db.relationship(Teacher)

class Student(UserMixin ,db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text)
    email = db.Column(db.String(255), unique = True)
    phone = db.Column(db.Integer, unique= True)
    password = db.Column(db.String(120))
    comment = db.relationship('Comment', backref="student", lazy = True)
    saved = db.Column(db.String)
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return Student.query.filter_by(email=self.email).first()
    def get_student(self):
        return{
            "id" : self.id,
            "name": self.name,
            "desc" : self.desc,
            "avata_url" : self.avata_url,
            "email": self.email,
            "phone": self.phone,
            "saved": self.saved
        }
class TokenStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    user = db.relationship(Student)
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    recourse_id = db.Column(db.Integer, db.ForeignKey('recourses.id'), nullable=False)
    recomments = db.relationship("Recomment", backref="comment", lazy = True)
    def get_comment(self):
        return{
            "id": self.id,
            "body": self.body,
            "user_id": self.student.get_student(),
            "recourse_id": self.recourse_id,
            "recomment": [recomment.get_recomment() for recomment in self.recomments]
        }
class Recomment(db.Model):
    __tablename__ = 'recomments'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable = False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable = False)
    def get_recomment(self):
        return{
            "id": self.id,
            "body": self.body,
            "user_id": self.user_id,
            "comment_id": self.comment_id
        }
