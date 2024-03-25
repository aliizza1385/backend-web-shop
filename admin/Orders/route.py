from flask import Blueprint, jsonify, request
from .models import Order
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
from admin.OrderItem.models import OrderItem


blueprint = Blueprint('order', __name__)
    

@blueprint.route('/order', methods=["GET"])
def orders():
    orders = Order.query.all()
    all_orders = []
    for order in orders:
        all_orders.append({
            "id":order.id,
            'order_date':order.order_date,
            'total_amount':order.total_amount,
            'status':order.status,
            'customer':order.customer.username,

        })
    response = jsonify(all_orders)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_orders)
    return response


# @blueprint.route('/order/<int:id>', methods=["GET"])
# def show_one_user(id):
#     one_order = Orders.query.get_or_404(id)
#     if one_order is None:
#         return '', 404
#     return jsonify({
#           "id":one_order.id,
#             'products':one_order.products.name,
#             # 'order_details':one_order.order_details.quantity,
#             'status':one_order.status,
#             # 'unit_price':one_order.order_details.unit_price,
#     })



@blueprint.route('/order/<int:id>', methods=["GET"])
def show_one_order(id):
    one_order = Order.query.get_or_404(id)

    All_order_item = []
    for i in one_order.orderitems:
        All_order_item.append({
            i.product.name,
            i.quantity
        })

    return jsonify({
        "id":one_order.id,
        'order_date':one_order.order_date,
        'status':one_order.status,
        'customer':one_order.customer.username,
        # 'items':All_order_item
    })


@blueprint.route('/order/<int:id>', methods=["PUT"])
def update_order(id):
    # Check if user exists
    order_update = Order.query.get_or_404(id)
    
    status = request.json.get('status', "").strip()
    
    print(status)
    # Update user data if provided
    if status:
        order_update.status = status
        db.session.commit()

    return jsonify({
        "id":order_update.id,
        'order_date':order_update.order_date,
        'total_amount':order_update.total_amount,
        'status':order_update.status,
        'customer':order_update.customer.username,
        'status':order_update.status,

    })





@blueprint.route('/users/<int:id>', methods=["DELETE"])
def DELETE_one_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    order = {
        "id":order.id,
        'order_date':order.order_date,
        'total_amount':order.total_amount,
        'status':order.status,
        'customer':order.customer.username,
    }
    return jsonify(user)
    