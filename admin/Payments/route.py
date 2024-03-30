from flask import Blueprint, jsonify, request
from .models import Payment
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db


blueprint = Blueprint('payment', __name__)



@blueprint.route('/payment', methods=["GET"])
def payment():
    p = Payment.query.all()
    all_payment = []
    for payment_in_for in p:
        all_payment.append({
            "id":payment_in_for.id,
            'order_id':payment_in_for.order_id,
            'payment_method':payment_in_for.payment_method,
            'amount':payment_in_for.amount,
            'payment_date':payment_in_for.payment_date,
        })


    response = jsonify(all_payment)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_payment)
    return response


@blueprint.route('/payment/<int:id>', methods=["GET"])
def show_one_payment(id):
    one_payment = Payment.query.get_or_404(id)
    if one_payment is None:
        return '', 404
    return jsonify({
        "id":one_payment.id,
        'order_id':one_payment.order_id,
        'payment_method':one_payment.payment_method,
        'amount':one_payment.amount,
        'payment_date':one_payment.payment_date,
    })

