from flask import Blueprint, render_template,request,flash, redirect,url_for, jsonify
from flask_login import current_user, login_required, login_user,logout_user
from src import db, app
from src.models import Teacher


teacher_blueprint = Blueprint('teachers', __name__)

@teacher_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data["email"]
        password = data["pass"]
        check_mail = Teacher.query.filter_by(email = email).first()
        print('check',check_mail)
        if check_mail.check_password:
            print('email', email)
            return jsonify({'email': email,
                            'name': check_mail.name, 
                            "desc": check_mail.desc, 
                            "avata_url": check_mail.avata_url, 
                            "phone": check_mail.phone, 
                            "course_id": check_mail.course_id,
                            "recourse_id": check_mail.recourse_id
                            })
        if not check_mail:
            return jsonify({'email': 'not exits'})
    return jsonify({'email': 'not exits'})
