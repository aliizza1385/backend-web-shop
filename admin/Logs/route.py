from flask import Blueprint, jsonify, request
from .models import Logs
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
import ast


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
    # Parse the search filter from the request arguments
    search = ast.literal_eval(request.args.get("filter"))

    if not search:
        log = Logs.query.all()

    else:
        # Query the Payment table based on the search filter
        log = Logs.query.filter(
            (Logs.user_id.ilike(f'%{search["name"]}%')) |
            (Logs.action.ilike(f'%{search["name"]}%')) |
            (Logs.action_date.ilike(f'%{search["name"]}%'))
        ).all()

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

    