from flask import Blueprint, render_template, request, redirect, url_for,jsonify

from initialize import db
from admin.Categori.models import Category
from admin.Products.models import Product
from admin.OrderItem.models import OrderItem
from admin.Orders.models import Order
from config import UPLOAD_FOLDER, localhost
from flask_login import current_user


# Create a Blueprint named 'login'
blueprint = Blueprint('shop', __name__)


@blueprint.route('/shop')
def shop():
    categories = Category.query.all()
    products = Product.query.all()

    return render_template('shop.html', categories = categories,products=products)

@blueprint.route('/<int:id>')
def category_by_id(id):
    categories = Category.query.all()
    products = Product.query.filter(Product.category_id == id)

    return render_template('shop.html', categories = categories,products=products)


@blueprint.route('/detail/<int:product_id>')
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('product-details.html', product = product)

@blueprint.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.form.get('quantity')
    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item

    if not order: # create a cart order if not exist
        order = Order(customer_id=current_user.id,status='cart')
        db.session.add(order)
        db.session.commit()

    order_item = None # check for dublicates orderItems
    for item in order.orderitems:
        if item.product.id == id:
            order_item = item
    information_product = Product.query.get(product_id)
    if not order_item: # create order item if not exist
        order_item = OrderItem(order_id=order.id,product_id=product_id,quantity=quantity,unit_price=information_product.price)
        db.session.add(order_item)
        db.session.commit()
    else:
        order_item.quantity += quantity # add quantity if exist
        db.session.commit()
    
    # return redirect(url_for('site.product',id=id))
    return render_template('shop-cart.html', orders=order.orderitems)


@blueprint.route('/delete/<int:product_id>')
def delete_in_cart(product_id):
    orderitem = OrderItem.query.get_or_404(product_id)
    db.session.delete(orderitem)
    db.session.commit()
    return redirect(url_for('shop.cart'))



@blueprint.route('/cart', methods=["GET","POST"])
def cart():
    context = {}
    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item
    context['order'] = order

    if request.method == "GET":
        return render_template('profile_customer.html',**context)
    
    elif request.method == 'POST':
        for item in order.orderitems:
            item.quantity = request.form.get(str(item.id)) # gets new quantity from cart
            db.session.commit()
        return redirect(url_for('ordering.checkout',id=order.id))


