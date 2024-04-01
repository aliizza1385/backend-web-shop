from flask import Blueprint, jsonify, request
from .models import Logs
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db


blueprint = Blueprint('Logs', __name__)


def get_log_and_save_then(action,ip_address):
    
    user_id = request.headers.get("user")
    # Create a new log and save it to the database
    new_Logs = Logs(action=action, user_id=user_id, ip_address=ip_address)
    db.session.add(new_Logs)
    db.session.commit()

    # Return a success message
    return jsonify({
        "id": new_Logs.id,
        'action': new_Logs.action,
        'user_id': new_Logs.user_id,
        'ip_address': new_Logs.ip_address,
    })

    

    

@blueprint.route('/log', methods=["GET"])
def log():
    log = Logs.query.all()
    all_log = []

    for log_in_for in log:
        all_log.append({
            "id":log_in_for.user_id,
            'user_id':log_in_for.user_id,
            'action':log_in_for.action,
            'action_date':log_in_for.action_date,
            'ip_address':log_in_for.ip_address,
            # 'password':customer.password
        })
    response = jsonify(all_log)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_log)
    return response


# @blueprint.route('/feedback/<int:id>', methods=["GET"])
# def show_one_feedback(id):
#     one_feedback = Feedback.query.get_or_404(id)
#     if one_feedback is None:
#         return '', 404
#     return jsonify({
#         "id":one_feedback.id,
#         'usernmae': one_feedback.customer.username,
#         'comment': one_feedback.comment,
#         'rating': one_feedback.rating,
#     })