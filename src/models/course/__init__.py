from src import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    img = db.Column(db.Text)
    desc = db.Column(db.Text)
    subject = db.Column(db.String, nullable=False)
    recourse_id = db.relationship('Recourse', backref='course', lazy = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    def render(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc,
            'recourse_id': self.recourse_id,
            'teacher_id': self.teacher_id
        }