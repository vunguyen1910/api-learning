from flask import Blueprint, request, jsonify
from src import db
from src.models import Course, Recourse

recourse_blueprint = Blueprint('recourses', __name__)


@recourse_blueprint.route('/<id>')
def get_recourse(id):
    recourse_from_course = Recourse.query.filter_by(course_id = id).all()
    return jsonify(data=[row.render() for row in recourse_from_course])


@recourse_blueprint.route('/create', methods=['POST'])
def create_recourse():
    if request.method == "POST":
        data = request.get_json()
        recourseURL = data['url']
        recourseTitle = data['title']
        recourseDesc = data['desc']
        recourseTeacher = data['teacher_id']
        recourseIDCourse = data['course_id']
        check_url = Recourse.query.filter_by(url=recourseURL).first()

        if not check_url:
            new_reCourse = Recourse(url=recourseURL, title=recourseTitle, desc=recourseDesc,
                                    course_id=recourseIDCourse, teacher_id=recourseTeacher)
            db.session.add(new_reCourse)
            db.session.commit()
            return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})

@recourse_blueprint.route('/<id>/delete', methods=['DELETE'])
def delete_recourse():
    if request.method == 'DELETE':
        recourse = Recourse.query.filter_by(id = id).first()
        db.session.delete(recourse)
        db.session.commit()
        return jsonify({'message': f'course {id} has deleted'})

@recourse_blueprint.route('/<id>/edit', methods=['PUT'])
def edit_recourse(id):
    if request.method == 'PUT':
        recourse = Recourse.query.filter_by(id = id).first()
        data = request.get_json()
        urlRecourse = data['url']
        titleRecourse = data['title']
        descRecourse = data['desc']

        recourse.url = urlRecourse
        recourse.title = titleRecourse
        descRecourse = descRecourse

        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


