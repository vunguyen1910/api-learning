from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from src import db, app
from src.models import Teacher, Token
import uuid

teacher_blueprint = Blueprint('teachers', __name__)

@teacher_blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
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
                return jsonify({"user": {'email': email,
                                         'name': check_user.name,
                                         "desc": check_user.desc,
                                         "avata_url": check_user.avata_url,
                                         "phone": check_user.phone,
                                         "course_id": check_user.course_id,
                                         "recourse_id": check_user.recourse_id},
                                "token": token.uuid,
                                "success": True,
                                "message": "success"
                                })
            return jsonify({"success": False,
                            'message': 'Wrong Pass'})
    return jsonify({"success": False,
                    'message': 'Email not exits'})


@app.route("/logout")
@login_required
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    if token:
        db.session.delete(token)
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
        check_email = Teacher.query.filter_by(email=email_user).first()
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
            new_token = token = Token(
                user_id=new_teacher.id, uuid=str(uuid.uuid4().hex))
            db.session.add(new_teacher, new_token)
            db.session.commit()
            return jsonify({'email': email_user,
                            'name': check_email.name,
                            "desc": check_email.desc,
                            "avata_url": check_email.avata_url,
                            "phone": check_email.phone,
                            "course_id": check_email.course_id,
                            "recourse_id": check_email.recourse_id,
                            "token": token.uuid,
                            "state": "success"
                            })
        if check_phone:
            return jsonify({'state': 'phone already exits'})
        if check_name:
            return jsonify({'state': 'name already exits'})
        return jsonify({'state': 'email already exits'})
    return jsonify({'state: pls login'})


@teacher_blueprint.route('/getuser', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        "name": current_user.name,
        "id": current_user.id,
        "email": current_user.email
    })
