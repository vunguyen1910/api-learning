from src import db
from src.models import Teacher

class Recourse(db.Model):
    __tablename__ = 'recourses'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text, unique = True, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    desc = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    document_id = db.relationship('Document', backref='recourse', lazy = True)
    
    def render(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "desc": self.desc,
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'document_id': self.document_id
        }

class Document(db.Model):
    __tablename__="documents"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    title = db.Column(db.String(255), nullable = False)
    desc = db.Column(db.String(190))
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=False)
    user = db.relationship(Teacher)
    recoures_id = db.Column(db.Integer, db.ForeignKey('recourses.id'))