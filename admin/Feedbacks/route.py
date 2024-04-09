from flask import Blueprint, jsonify, request
from .models import Feedback
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
import ast

blueprint = Blueprint('feedback', __name__)


    

@blueprint.route('/feedback', methods=["GET"])
def feedback():
    # Parse the search filter from the request arguments
    search = ast.literal_eval(request.args.get("filter"))
    if not search:
        feedback = Feedback.query.all()

    else:
        # Query the Payment table based on the search filter
        feedback = Feedback.query.filter(
            (Feedback.customer_id.ilike(f'%{search["name"]}%')) |
            (Feedback.rating.ilike(f'%{search["name"]}%')) |
            (Feedback.order_id.ilike(f'%{search["name"]}%'))
        ).all()
    
    all_feedback = []
    for feedback_in_for in feedback:
        all_feedback.append({
            "id":feedback_in_for.id,
            'usernmae':feedback_in_for.customer.username,
            'order_id':feedback_in_for.order_id,
            'rating':feedback_in_for.rating,
            'feedback_date':feedback_in_for.feedback_date,
            'comment':feedback_in_for.comment,
        })

# Create a JSON response with the payment data
    response = jsonify(all_feedback)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = str(len(all_feedback))
    return response



@blueprint.route('/feedback/<int:id>', methods=["GET"])
def show_one_feedback(id):
    one_feedback = Feedback.query.get_or_404(id)
    if one_feedback is None:
        return '', 404
    return jsonify({
        "id":one_feedback.id,
        'usernmae': one_feedback.customer.username,
        'comment': one_feedback.comment,
        'rating': one_feedback.rating,
    })