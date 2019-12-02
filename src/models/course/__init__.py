from src import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    img = db.Column(db.Text, nullable = False)
    desc = db.Column(db.Text)
    recourse_id = db.relationship('Recourse', backref='course', lazy = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    students = db.relationship('Student', secondary = "StudentCourse", lazy='subquery', backref = db.backref('courses', lazy = True))