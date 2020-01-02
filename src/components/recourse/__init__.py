from flask import Blueprint, request, jsonify
from src import db
from src.models import Course, Recourse, Document, User, Notification
from src.models.teacher import Comment, Recomment
from flask_login import current_user, login_required, login_user, logout_user

recourse_blueprint = Blueprint('recourses', __name__)

@recourse_blueprint.route('/<id>')
def get_recourse(id):
    recourse_from_course = Recourse.query.filter_by(course_id=id).all()
    return jsonify(data=[row.render() for row in recourse_from_course])
    
@recourse_blueprint.route('/singel-recourse/<id>')
def get_singel_course(id):
    recourse_singel = Recourse.query.filter_by(id = id).first()
    print(recourse_singel.id,"recourse singel here")
    return jsonify(data = recourse_singel.render())

@recourse_blueprint.route('/create', methods=['POST'])
@login_required
def create_recourse():
    if request.method == "POST":
        data = request.get_json()
        recourseURL = data['url']
        recourseTitle = data['title']
        recourseDesc = data['desc']
        recourseIDCourse = data['course_id']
        check_url = Recourse.query.filter_by(url=recourseURL).first()
        if current_user.role == "teacher":
            if not check_url:
                new_reCourse = Recourse(url=recourseURL, title=recourseTitle, desc=recourseDesc,
                                        course_id=recourseIDCourse, user_id=current_user.id)
                user = User.query.filter_by(id = current_user.id).first()
                user.score = user.score + 3
                db.session.add(new_reCourse)
                db.session.commit()
                return jsonify({"success": True})
            return jsonify({"success": False})
        return jsonify({"success": False})


@recourse_blueprint.route('/<id>/delete', methods=['DELETE'])
@login_required
def delete_recourse(id):
    if request.method == 'DELETE':
        recourse = Recourse.query.filter_by(id=id).first()
        if recourse.user_id == current_user.id:
            user = User.query.filter_by(id = current_user.id).first()
            user.score = user.score - 3
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
                           recoures_id=recourse_id, user_id=current_user.id)
        user = User.query.filter_by(id = current_user.id).first()
        user.score = user.score + 3
        db.session.add(new_doc)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

@recourse_blueprint.route("/<id>/delete-doc", methods=['DELETE'])
@login_required
def delete_document(id):
    if request.method == 'DELETE':
        document_need_to_delete = Document.query.filter_by(id = id).first()
        user = User.query.filter_by(id = current_user.id).first()
        user.score = user.score - 3
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

@recourse_blueprint.route('/<id>/create-comment', methods=['POST'])
@login_required
def create_comment(id):
    if request.method == "POST":
        data = request.get_json()
        comment = data['comment']
        new_comment = Comment(body = comment, user_id = current_user.id, recourse_id = id)
        db.session.add(new_comment)
        db.session.commit()
        print(new_comment.id, "id comment")
        recourse = Recourse.query.get(id)
        new_notice = Notification(sender_id = current_user.id, comment_id=new_comment.id, post_id = id, recipient_id = recourse.user_id, body = f'{current_user.name} has comment on your post') 
        db.session.add(new_notice)
        db.session.commit()
        return jsonify({'success': False})
    return jsonify({"success": False})
@recourse_blueprint.route('/<id>/delete-comment', methods=['DELETE'])
@login_required
def delete_comment(id):
    if request.method == "DELETE":
        comment = Comment.query.filter_by(id =id).first()
        if current_user.id == comment.user_id:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False})
    return jsonify({"success": False})

@recourse_blueprint.route('/<id>/create-recomment', methods=['POST'])
@login_required
def create_recomment(id):
    if request.method == "POST":
        data = request.get_json()
        recomment = data['recomment']
        if current_user.role == "teacher":
            comment = Comment.query.filter_by(id = id).first()
            user = User.query.filter_by(id = current_user.id).first()
            user.score = user.score + 2
            new_recomment = Recomment(body = recomment, post_id = comment.recourse_id, user_id = current_user.id, comment_id = id)
            new_notice = Notification(sender_id = current_user.id, comment_id=comment.id ,post_id = comment.recourse_id, recipient_id = comment.user_id, body = f'{current_user.name} has answer on your comment')
            db.session.add(new_notice)
            db.session.add(new_recomment)
            db.session.commit()
            return jsonify({"success": True})
        return jsonify({"success": False})
    return jsonify({"success": False})

@recourse_blueprint.route('/<id>/delete-recomment', methods=['DELETE'])
@login_required
def delete_recomment(id):
    if request.method == "DELETE":
        recomment = Recomment.query.filter_by(id =id).first()
        if current_user.id == recomment.user_id:
            user = User.query.filter_by(id = current_user.id).first()
            user.score = user.score - 2
            db.session.delete(recomment)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False})
    return jsonify({"success": False})