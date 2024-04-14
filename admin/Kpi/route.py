from flask import Blueprint, jsonify, request
from initialize import db
import sqlite3
from admin.Products.models import Product
from admin.Orders.models import Order
from admin.OrderItem.models import OrderItem


blueprint = Blueprint('kpi', __name__)



@blueprint.route('/kpi', methods=["GET"])
def KPI():
    products = []
    for product in Product.query.all():
        count = 0
        for orderitem in OrderItem.query.all():
            if orderitem.order.status != "cart" and orderitem.product == product:
                count += orderitem.quantity
        products.append({
            'id':product.id,
            'name':product.name,
            'sales':count
        })
    response = jsonify(products)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(products)
    return response
