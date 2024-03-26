from flask import Blueprint, jsonify, request
from .models import Feedback
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db


blueprint = Blueprint('feedback', __name__)


    

@blueprint.route('/feedback', methods=["GET"])
def feedback():
    feedback = Feedback.query.all()
    all_feedback = []
    for feedback_in_for in feedback:
        all_feedback.append({
            "id":feedback_in_for.id,
            'usernmae':feedback_in_for.customer.username,
            'order_id':feedback_in_for.order_id,
            'rating':feedback_in_for.rating,
            'feedback_date':feedback_in_for.feedback_date,
            'comment':feedback_in_for.comment,
            # 'password':customer.password
        })
    response = jsonify(all_feedback)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_feedback)
    return response


# @blueprint.route('/customers/<int:id>', methods=["GET"])
# def show_one_product(id):
#     one_customer = Customer.query.get_or_404(id)
#     if one_customer is None:
#         return '', 404
#     return jsonify({
#         "id":one_customer.id,
#         'username': one_customer.username,
#         'email': one_customer.email,
#         'phone_number': one_customer.phone_number,
#         'registration_date': one_customer.registration_date,
#         'password': one_customer.password,
#     })



    



# @blueprint.route('/customers/<int:id>', methods=["DELETE"])
# def DELETE_one_customer(id):
#     customer = Customer.query.get_or_404(id)
#     db.session.delete(customer)
#     db.session.commit()
#     customer = {
#         "id": customer.id,
#         'username': customer.username,
#         'email': customer.email,
#         'phone_number': customer.phone_number,
#     }
#     return jsonify(customer)
    