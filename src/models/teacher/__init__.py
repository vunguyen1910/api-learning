from flask_login import UserMixin
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text)
    email = db.Column(db.String(255), unique = True, nullable = False)
    phone = db.Column(db.Integer, unique= True)
    course_id = db.relationship('Course', backref='teacher', lazy = True)
    recourse_id = db.relationship('Recourse', backref='teacher', lazy = True)
    password = db.Column(db.String(120),nullable=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return User.query.filter_by(email=self.email).first()
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=False)
    user = db.relationship(Teacher)

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable = False)
    user = db.relationship(Teacher)