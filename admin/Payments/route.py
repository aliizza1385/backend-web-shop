from flask import Blueprint, jsonify, request
from .models import Payment
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
import ast

blueprint = Blueprint('payment', __name__)


# def search_payment():
#     # Get the search query from the request
#     search_query = request.args.get('name', '')

#     # Query the database to filter payments based on the search query
#     filtered_payments = Payment.query.filter(Payment.order_id.ilike(f'%{search_query}%')).all()

#     # Convert the filtered payments to a list of dictionaries
#     for payment in filtered_payments:
#         result = [
#             {
#                 "id": payment.id,
#                 "order_id": payment.order_id,
#                 "payment_method": payment.payment_method,
#                 "amount": payment.amount,
#                 # "payment_date": payment.payment_date.strftime('%Y-%m-%d')
#             }
#         ]

#     return jsonify(result)

@blueprint.route('/payment', methods=["GET"])
def payment():
    try:
        # Parse the search filter from the request arguments
        search = ast.literal_eval(request.args.get("filter"))
        if not search:
            p = Payment.query.all()
        else:
            # Query the Payment table based on the search filter
            p = Payment.query.filter(
                (Payment.order_id.ilike(f'%{search["name"]}%')) |
                (Payment.payment_method.ilike(f'%{search["name"]}%')) |
                (Payment.payment_date.ilike(f'%{search["name"]}%'))
            ).all()

        # Create a list to store the payment data
        all_payment = []
        for payment_in_for in p:
            all_payment.append({
                "id": payment_in_for.id,
                'order_id': payment_in_for.order_id,
                'payment_method': payment_in_for.payment_method,
                'amount': payment_in_for.amount,
                'payment_date': payment_in_for.payment_date,
            })

        # Create a JSON response with the payment data
        response = jsonify(all_payment)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers['Content-Range'] = str(len(all_payment))
        return response

    except Exception as e:
        return jsonify({"error": str(e)})


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

