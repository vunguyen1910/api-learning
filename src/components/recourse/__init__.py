from flask import Blueprint, request, jsonify
from src import db
from src.models import Course, Recourse, Document
from flask_login import current_user, login_required, login_user, logout_user

recourse_blueprint = Blueprint('recourses', __name__)



@recourse_blueprint.route('/<id>')
def get_recourse(id):
    recourse_from_course = Recourse.query.filter_by(course_id=id).all()
    return jsonify(data=[row.render() for row in recourse_from_course])
    
@recourse_blueprint.route('/singel-recourse/<id>')
def get_singel_course(id):
    recourse_singel = Recourse.query.filter_by(course_id=id).first()
    return jsonify({
        "data":{
            "id" : recourse_singel.id,
            "url" : recourse_singel.url,
            "title" : recourse_singel.title,
            "desc" : recourse_singel.desc,
            "course_id" : recourse_singel.course_id,
            "teacher_id" : recourse_singel.teacher_id            
        }
    })

@recourse_blueprint.route('/create', methods=['POST'])
@login_required
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
@login_required
def delete_recourse():
    if request.method == 'DELETE':
        recourse = Recourse.query.filter_by(id=id).first()
        db.session.delete(recourse)
        db.session.commit()
        return jsonify({'message': f'course {id} has deleted'})


@recourse_blueprint.route('/<id>/edit', methods=['PUT'])
@login_required
def edit_recourse(id):
    if request.method == 'PUT':
        recourse = Recourse.query.filter_by(id=id).first()
        data = request.get_json()
        urlRecourse = data['url']
        titleRecourse = data['title']
        descRecourse = data['desc']

        recourse.url = urlRecourse
        recourse.title = titleRecourse
        recourse.desc = descRecourse

        db.session.commit()
        
        return jsonify({'success': True})
    return jsonify({'success': False})


@recourse_blueprint.route("/create-document", methods=['POST'])
@login_required
def create_document():
    if request.method == "POST":
        data = request.get_json()
        titleDoc = data['title']
        bodyDoc = data['body']
        recourse_id = data['recourse_id']
        new_doc = Document(text=bodyDoc, title=titleDoc,
                           recoures_id=recourse_id, teacher_id=current_user.id)
        db.session.add(new_doc)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@recourse_blueprint.route("/<id>/render_document")
def render_document(id):
    all_doc = Document.query.filter_by(recoures_id = id).all()
    return jsonify(data=[row.render() for row in all_doc])

@recourse_blueprint.route("/<id>/delete-doc", methods=['DELETE'])
@login_required
def delete_document(id):
    if request.method == 'DELETE':
        document_need_to_delete = Document.query.filter_by(id = id).first()
        db.session.delete(document_need_to_delete)
        db.session.commit()
        return jsonify({'success': True})

@recourse_blueprint.route('/<id>/edit-doc', methods=['PUT'])
@login_required
def edit_document(id):
    if request.method == 'PUT':
        fix_doc = Document.query.filter_by(id = id).first()
        data = request.get_json()
        newTitle = data['title']
        newBody = data['body']

        fix_doc.title = newTitle
        fix_doc.text = newBody

        print(fix_doc.title,"new title?")
        print(fix_doc.text, "new body?")
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})