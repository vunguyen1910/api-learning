from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from src import db, app, mail
from src.models import Teacher, Token
from src.models.teacher import Student, TokenStudent
import uuid
import requests
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
teacher_blueprint = Blueprint('teachers', __name__)
from flask_mail import Message

@teacher_blueprint.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        data = request.get_json()
        role = data['role']
        email = data['email']
        if role == 'teacher':       
            check_user = Teacher.query.filter_by(email=email).first()
            if check_user:
                if check_user.check_password(data['pass']):
                    token = Token.query.filter_by(user_id=check_user.id).first()
                    if not token:
                        token = Token(user_id=check_user.id,
                                    uuid=str(uuid.uuid4().hex))
                        db.session.add(token)
                        db.session.commit()
                    login_user(check_user)
                    return jsonify({"user": check_user.get_teacher(),
                                    "token": token.uuid,
                                    "role" : "teacher",
                                    "success": True,
                                    })
                return jsonify({"success": False,
                                'message': 'Wrong Pass'})
            return jsonify({"success": False,
                            'message': 'Email not exits'})
        if role == "student":
            check_user = Student.query.filter_by(email = email).first()
            if check_user:
                if check_user.check_password(data['pass']):
                    token = TokenStudent.query.filter_by(user_id=check_user.id).first()
                    if not token:
                        token = TokenStudent(user_id=check_user.id,
                                    uuid=str(uuid.uuid4().hex))
                        db.session.add(token)
                        db.session.commit()
                    login_user(check_user)
                    return jsonify({"user": check_user.get_student(),
                                    "token": token.uuid,
                                    "role": "student",
                                    "success": True,
                                    })
                return jsonify({"success": False,
                                'message': 'Wrong Pass'})
            return jsonify({"success": False,
                            'message': 'Email not exits'})


@teacher_blueprint.route("/logout")
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    if token:
        db.session.delete(token)
        db.session.commit()
    if not token:
        tokenStudent = TokenStudent.query.filter_by(user_id = current_user.id).first()
        db.session.delete(tokenStudent)
        db.session.commit()
    logout_user()
    return jsonify({
        'success': True
    })


@teacher_blueprint.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email_user = data['email']
        role = data['role']
        if role == 'teacher':
            check_email = Teacher.query.filter_by(email = email_user).first()
            check_phone = Teacher.query.filter_by(phone=data['phone']).first()
            check_name = Teacher.query.filter_by(name=data['name']).first()
            if not check_email and not check_phone and not check_name:
                new_teacher = Teacher(email=email_user,
                                    name=data['name'],
                                    desc=data['desc'],
                                    avata_url=data['avata_url'],
                                    phone=data['phone']
                                    )
                new_teacher.set_password(data['password'])
                db.session.add(new_teacher)
                db.session.commit()
                return jsonify({"user":{
                                'id': new_teacher.id,
                                'email': email_user,
                                'name': new_teacher.name,
                                "desc": new_teacher.desc,
                                "avata_url": new_teacher.avata_url,
                                "phone": new_teacher.phone,
                                },
                                "success": True
                                })
            if check_phone:
                return jsonify({'state': 'phone already exits', "success": False})
            if check_name:
                return jsonify({'state': 'name already exits' , "success": False})
            return jsonify({'state': 'email already exits' , "success": False})

        if role == "student":
            check_email = Student.query.filter_by(email = email_user).first()
            check_phone = Student.query.filter_by(phone=data['phone']).first()
            check_name = Student.query.filter_by(name=data['name']).first()
            if not check_email and not check_phone and not check_name:
                new_student = Student(email=email_user,
                                    name=data['name'],
                                    desc=data['desc'],
                                    avata_url=data['avata_url'],
                                    phone=data['phone']
                                    )
                new_student.set_password(data['password'])
                db.session.add(new_student)
                db.session.commit()
                return jsonify({"user":{
                                'id': new_student.id,
                                'email': email_user,
                                'name': new_student.name,
                                "desc": new_student.desc,
                                "avata_url": new_student.avata_url,
                                "phone": new_student.phone,
                                },
                                "success": True
                                })
            if check_phone:
                return jsonify({'state': 'phone already exits', "success": False})
            if check_name:
                return jsonify({'state': 'name already exits' , "success": False})
            return jsonify({'state': 'email already exits' , "success": False})

    return jsonify({"success": False})


@teacher_blueprint.route('/getuser', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        "name": current_user.name,
        "id": current_user.id,
        "email": current_user.email
    })


def send_email(token, email, name):
    with app.app_context():
        try:
            msg = Message(subject="Reset your password from learning music",
                        sender=app.config.get("MAIL_USERNAME"), #sender email
                        recipients=[email],
                        body= f"Hi! {name} to reset your email please enter the link : https://learning-music-online.netlify.com/new-password/?token={token}")
            mail.send(msg)
        except Exception as err:
            print(f'{err}')
        else: print("success!")

@teacher_blueprint.route('/forgot-password', methods = ['POST'])
def get_password():
    if request.method == 'POST':
        data = request.get_json()
        teacher = Teacher.query.filter_by(email = data['email']).first()
        if not teacher:
            student = Student.query.filter_by(email = data['email']).first()
            if not student:
                return jsonify({'success': False,
                                'wrong': 'email does not exist'}
                )
            else:
                s = URLSafeTimedSerializer(app.secret_key)
                token = s.dumps(student.email, salt="RESET_PASSWORD")
                send_email(token, student.email, student.name)
                return jsonify({"success": True, 'right': 'email has sent'})

        else:
            s = URLSafeTimedSerializer(app.secret_key)
            token = s.dumps(teacher.email, salt="RESET_PASSWORD")
            send_email(token, teacher.email, teacher.name)
            return jsonify({"success": True, 'right': 'email has sent'})
    return jsonify({'success': False, 'state': 'input your email'})

@teacher_blueprint.route('/new-password', methods = ['POST'])
def get_new_password():
    data = request.get_json()
    token = data['token']
    new_password = data['password']
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(token, salt="RESET_PASSWORD")
    teacher = Teacher(email = email).check_user()
    if not teacher:
        student = Student(email = email).check_user()
        if not student:
            print("INVALID_TOKEN")
            return redirect("https://learning-music-online.netlify.com/forgot-password")
        else:
            student.set_password(new_password)
            db.session.commit()
            return jsonify({"success": True})
    else:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": False})
    


