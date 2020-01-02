from src import db
from src.models import User, Notification
from src.models.teacher import Comment

class Recourse(db.Model):
    __tablename__ = 'recourses'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text, unique = True, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    desc = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    documents = db.relationship('Document', backref='recourse', lazy = True)
    comments = db.relationship("Comment", backref="recourse", lazy="dynamic")
    notification = db.relationship("Notification", backref="recourse", lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    def render(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "desc": self.desc,
            'course_id': self.course_id,
            'author': User.query.get(self.user_id).get_user(),
            "document": [document.render() for document in self.documents],
            'comments': [comment.get_comment() for comment in self.comments.order_by(Comment.id.desc()).all()],
            "date": self.updated_at
        }
class Document(db.Model):
    __tablename__="documents"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    recoures_id = db.Column(db.Integer, db.ForeignKey('recourses.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    def render(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.text,
            'recoures_id': self.recoures_id,
            'user_id': self.user_id,
            "date": self.updated_at
        }