from flask_login import UserMixin
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), nullable = False)
    desc = db.Column(db.Text)
    avata_url = db.Column(db.Text)
    email = db.Column(db.String(255), unique = True)
    phone = db.Column(db.Integer, unique= True)
    course_id = db.relationship('Course', backref='user', lazy = True)
    recourse_id = db.relationship('Recourse', backref='user', lazy = True)
    password = db.Column(db.String(120))
    score = db.Column(db.Integer)
    role = db.Column(db.String(10), default="student")
    comments = db.relationship("Comment", backref="user", lazy = True)
    recomments = db.relationship("Recomment", backref="user", lazy = True)
    messages_send = db.relationship("Notification", foreign_keys='Notification.sender_id', backref="usersend", lazy = 'dynamic')
    messages_received = db.relationship("Notification", foreign_keys='Notification.recipient_id', backref="userreciver", lazy = 'dynamic')

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def check_user(self):
        return User.query.filter_by(email=self.email).first()
    def get_user(self):
        return{
            "id" : self.id,
            "name": self.name,
            "desc": self.desc,
            "avata_url": self.avata_url,
            "email": self.email,
            "phone": self.phone,
            "score": self.score,
            "role" : self.role
        }

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    user = db.relationship(User)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recourse_id = db.Column(db.Integer, db.ForeignKey('recourses.id'), nullable=False)
    recomments = db.relationship("Recomment", backref="comment", lazy = True)
    def get_comment(self):
        return {
            "id": self.id,
            "body": self.body,
            "author": self.user.get_user(),
            "recomment": [recomment.get_recomment() for recommnet in self.recomments]
        }
class Recomment(db.Model):
    __tablename__ = "recomments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    def get_recomment(self):
        return{
            "id": self.id,
            "body": self.body,
            "author": self.user.get_user()
        }

class Notification(db.Model):
    __tablename__="notifications"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("recourses.id"))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    readed = db.Column(db.Boolean, default= False)
    def get_notification(self):
        return {
            "id": self.id,
            "body": self.body,
            "sender": self.usersend.get_user(),
            "recipient": self.userreciver.get_user(),
            "post_id": self.post_id,
            "readed": self.readed
        }