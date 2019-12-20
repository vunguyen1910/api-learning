from src import db
from src.models import User

class Recourse(db.Model):
    __tablename__ = 'recourses'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text, unique = True, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    desc = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    document_id = db.relationship('Document', backref='recourse', lazy = True)
    def render(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "desc": self.desc,
            'course_id': self.course_id,
            'user_id': self.user_id,
        }
class Document(db.Model):
    __tablename__="documents"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    recoures_id = db.Column(db.Integer, db.ForeignKey('recourses.id'))
    def render(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.text,
            'recoures_id': self.recoures_id,
            'user_id': self.user_id,
        }