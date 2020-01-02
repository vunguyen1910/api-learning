from src import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(155), unique = True, nullable = False)
    img = db.Column(db.Text)
    desc = db.Column(db.Text)
    subject = db.Column(db.String, nullable=False)
    recourse_id = db.relationship('Recourse', backref='course', lazy = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())

    def render(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "desc": self.desc,
            'user_id': self.user.get_user_secrect(),
            "date": self.updated_at
        }