from flask import Blueprint, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from src import db, app
from src.models import Course

course_blueprint = Blueprint('courses', __name__)

@course_blueprint.route('/create-post', methods = ["POST"])
@login_required
def create_Post():
    if request.method == 'POST':
        if current_user.role == "teacher":
            data = request.get_json()
            check_name = Course.query.filter_by(name = data['name']).first()
            if not check_name:
                new_course = Course(
                                    name= data['name'],
                                    img= data['img'],
                                    desc= data['desc'],
                                    subject= data['subject'],
                                    user_id= current_user.id
                )
                db.session.add(new_course)
                db.session.commit()
                return jsonify({'success': True})
            else: return jsonify({'success': False})
        return jsonify({"success": False})

@course_blueprint.route('/<subject>', methods = ['GET'])
def subject(subject):
    result = Course.query.filter_by(subject = subject).all()
    return jsonify(data=[row.render() for row in result])

@course_blueprint.route('/<id>/delete', methods = ['DELETE'])
@login_required
def deletePost(id):
    if request.method == "DELETE":
        course = Course.query.filter_by(id = id).first()
        if current_user.id == course.user_id:
            db.session.delete(course)
            db.session.commit()
            return jsonify({'message': f'course {id} has deleted'})
        return jsonify({'success': False})

@course_blueprint.route('/<id>/edit', methods = ['PUT'])
@login_required
def editCourse(id):
    if request.method == 'PUT':
        course = Course.query.filter_by(id = id).first()
        if current_user.id == course.id:
            data = request.get_json()
            newName = data['name']
            newImg = data['img']
            newDesc = data['desc']
            course.name = newName
            print (course.name)
            course.img = newImg
            course.desc = newDesc
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False})