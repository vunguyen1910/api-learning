from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from src import db, app, mail
from src.models import User, Token, Notification
import uuid
import requests
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
user_blueprint = Blueprint('users', __name__)
from flask_mail import Message

@user_blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        check_user = User.query.filter_by(email=email).first()
        if check_user:
            if check_user.check_password(data['pass']):
                token = Token.query.filter_by(user_id=check_user.id).first()
                if not token:
                    token = Token(user_id=check_user.id,
                                uuid=str(uuid.uuid4().hex))
                    db.session.add(token)
                    db.session.commit()
                login_user(check_user)
                return jsonify({"user": check_user.get_user(),
                                "token": token.uuid,
                                "success": True,
                                })
            return jsonify({"success": False,
                            'message': 'Wrong Pass'})
        return jsonify({"success": False,
                        'message': 'Email not exits'})


@user_blueprint.route("/logout")
def logout():
    token = Token.query.filter_by(user_id=current_user.id).first()
    db.session.delete(token)
    db.session.commit()
    logout_user()
    return jsonify({
        'success': True
    })

@user_blueprint.route("/edit-user/<id>", methods=["PUT"])
@login_required
def edit_user(id):
    if request.method == "PUT":
        user_edit = User.query.filter_by(id = id).first()
        if current_user.id == user_edit.id:
            data = request.get_json()
            email_user = data['email']
            user_edit.email = email_user
            user_edit.name = data['name']
            user_edit.desc = data["desc"]
            user_edit.avata_url = data['avata_url']
            user_edit.phone = data['phone']
            db.session.commit()         
            return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})

@user_blueprint.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email_user = data['email']
        role = data['role']
        check_email = User.query.filter_by(email = email_user).first()
        check_phone = User.query.filter_by(phone=data['phone']).first()
        check_name = User.query.filter_by(name=data['name']).first()
        if not check_email and not check_phone and not check_name:
            if role == 'teacher':
                new_user = User(email=email_user,
                                    name=data['name'],
                                    desc=data['desc'],
                                    avata_url=data['avata_url'],
                                    phone=data['phone'],
                                    role = data['role'],
                                    score = 0
                                    )
            if role == 'student':
                new_user = User(email=email_user,
                                name=data['name'],
                                desc=data['desc'],
                                avata_url=data['avata_url'],
                                phone=data['phone'],
                                role = data['role'],
                    )
            new_user.set_password(data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": True})
        if check_phone:
            return jsonify({'state': 'phone already exits', "success": False})
        if check_name:
            return jsonify({'state': 'name already exits' , "success": False})
        return jsonify({'state': 'email already exits' , "success": False})
    return jsonify({"success": False})


@user_blueprint.route('/getuser', methods=['GET'])
@login_required
def get_user():
    return jsonify({
        "user": current_user.get_user()
    })

@user_blueprint.route('/get-top-10')
def get_top_10():
    top10 = User.query.filter_by(role="teacher").order_by(User.score.desc()).limit(10).all()
    return jsonify({
        "user": [user.get_user_secrect() for user in top10]
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

@user_blueprint.route('/forgot-password', methods = ['POST'])
def get_password():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email = data['email']).first()
        if not user:
            return jsonify({'success': False,
                            'wrong': 'email does not exist'}
            )
        else:
            s = URLSafeTimedSerializer(app.secret_key)
            token = s.dumps(user.email, salt="RESET_PASSWORD")
            send_email(token, user.email, user.name)
            return jsonify({"success": True, 'right': 'email has sent'})
    return jsonify({'success': False, 'state': 'input your email'})

@user_blueprint.route('/new-password', methods = ['POST'])
def get_new_password():
    data = request.get_json()
    token = data['token']
    new_password = data['password']
    print(new_password, "newPass")
    s = URLSafeTimedSerializer(app.secret_key)
    email = s.loads(token, salt="RESET_PASSWORD")
    user = User(email = email).check_user()
    if not user:
        print("INVALID_TOKEN")
        return redirect("https://learning-music-online.netlify.com/forgot-password")
    else:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": True})

@user_blueprint.route('/notification', methods=['GET'])
@login_required
def get_notification():
    notices = Notification.query.filter_by(recipient_id = current_user.id).all()
    unseen = Notification.query.filter_by(readed = False).all()
    countUnseen = len(unseen)
    print(countUnseen)
    return jsonify({"data": [notice.get_notification() for notice in notices[::-1]], "countUnseen": countUnseen})

@user_blueprint.route('/notification/<id>', methods=['PUT'])
@login_required
def edit_notification(id):
    notice = Notification.query.filter_by(id = id).first()
    notice.readed = True
    db.session.commit()
    return jsonify({"success": True})

@user_blueprint.route('/notification/<id>/delete', methods=['DELETE'])
@login_required
def delete_notification(id):
    if request.method == "DELETE":
        notice_delete = Notification.query.filter_by(id = id).first()
        if current_user.id ==  notice_delete.recipient_id:
            db.session.delete(notice_delete)
            db.session.commit()
            return jsonify({"success": False})
        return jsonify({"success": False})
    return jsonify({"success": True})