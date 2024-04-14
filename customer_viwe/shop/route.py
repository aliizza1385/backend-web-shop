from flask import Blueprint, render_template, request, redirect, url_for,jsonify

from initialize import db
from admin.Categori.models import Category
from admin.Products.models import Product
from admin.OrderItem.models import OrderItem
from admin.Orders.models import Order
from config import UPLOAD_FOLDER, localhost
from flask_login import current_user
from admin.Customers.models import Customer
from admin.Address.models import Address
from admin.Payments.models import Payment

# Create a Blueprint named 'login'
blueprint = Blueprint('shop', __name__)


@blueprint.route('/shop')
def shop():
    categories = Category.query.all()
    products = Product.query.all()

    return render_template('shop.html', categories = categories,products=products, current_user =current_user)

@blueprint.route('/<int:id>')
def category_by_id(id):
    categories = Category.query.all()
    products = Product.query.filter(Product.category_id == id)

    return render_template('shop.html', categories = categories,products=products)


@blueprint.route('/detail/<int:product_id>')
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('product-details.html', product = product)


# @blueprint.route('/add_cart_shop/<int:customer_id>')
# def add_cart_shop(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
    
#     return render_template('shop-cart.html', orders=customer.orders.orderitems)

@blueprint.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = request.form.get('quantity')
    order = None 
    for item in current_user.orders:
        if item.status == "cart":
            order = item

    if not order: 
        order = Order(customer_id=current_user.id,status='cart')
        db.session.add(order)
        db.session.commit()

    order_item = None 
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
        return render_template('shop-cart.html',orders = order.orderitems,total_amount = order.total_amount,order_id = order.id)
    # print( order.total_amount)
    
    elif request.method == 'POST':
        for item in order.orderitems:
            item.quantity = request.form.get(str(item.id)) # gets new quantity from cart
            db.session.commit()
        return redirect(url_for('shop.checkout',id=order.id))
    


@blueprint.route('/checkout/<int:id>', methods=["GET","POST"])
def checkout(id):
    order = Order.query.get_or_404(id)
    context = {}
    context['order'] = order

    if request.method == "GET":
        return render_template('checkout.html',**context)
    
    elif request.method == 'POST':
        country = request.form.get('country')
        city = request.form.get('city')
        street = request.form.get('street')
        postal_code = request.form.get('postal_code')
        method = request.form.get('method')
        a = Address(order_id=order.id,country=country,city=city,
                        street=street,postal_code=postal_code)
        p = Payment(order_id=order.id,method=method,amount=order.total_amount)        
        order.status = 'sending'
        db.session.add(a)
        db.session.add(p)
        db.session.commit()
        flash("Order Placed !", 'info')
        return redirect (url_for('shop.dashboard'))
    
    
    
    
@blueprint.route('/dashboard', methods=["GET","POST"])
def dashboard():
    context = {}
    context['orders'] = Order.query.all()
    if request.method=="GET":
        return render_template('profile.html',**context)
    
    # if request.method=="POST":
    #     username = request.form.get('username',"").strip()
    #     password = request.form.get('password',"").strip()
    #     email = request.form.get('email',"").strip()

    #     current_user.username = username
    #     current_user.email = email
    #     if password:
    #         current_user.password = password
    #     db.session.commit()
    #     return render_template('ordering/dashboard.html',**context)


