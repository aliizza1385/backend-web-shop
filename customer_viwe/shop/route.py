from flask import Blueprint, render_template, request, redirect, url_for,jsonify,flash

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
from admin.Feedbacks.models import Feedback
from flask_login import login_user, current_user, logout_user, login_required

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
@login_required
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('product-details.html', product = product,localhost = localhost)

@blueprint.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
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
    print( order.id)
    return render_template('shop-cart.html', orders=order.orderitems,total_amount = order.total_amount,order_id = order.id)


@blueprint.route('/delete/<int:product_id>')
@login_required
def delete_in_cart(product_id):
    orderitem = OrderItem.query.get_or_404(product_id)
    db.session.delete(orderitem)
    db.session.commit()
    return redirect(url_for('shop.cart'))



@blueprint.route('/cart', methods=["GET","POST"])
@login_required
def cart():
    
    context = {}
    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item
    context['order'] = order
    if order is None:
        context['order'] = None
        return render_template('shop-cart.html', **context)
    
    elif request.method == "GET":
        return render_template('shop-cart.html',orders = order.orderitems,total_amount = order.total_amount,order_id = order.id)
    # print( order.total_amount)

    elif request.method == 'POST':
        for item in order.orderitems:
            item.quantity = request.form.get(str(item.id)) # gets new quantity from cart
            db.session.commit()
        return redirect(url_for('shop.shop',id=order.id))
    

    


@blueprint.route('/checkout/<int:id>', methods=["GET","POST"])
@login_required
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
        recipient = request.form.get('recipient')
        address_line1 = request.form.get('address_line1')
        address_line2 = request.form.get('address_line2')
        state = request.form.get('state')
        method = request.form.get('method')
        feedback = request.form.get('feedback')
        rating = request.form.get('rating')
        
        
        a = Address(customer_id = current_user.id,address_line1=address_line1,address_line2=address_line2,order_id=order.id,country=country,city=city,postal_code=postal_code,recipient_name=recipient,state=state)
        p = Payment(order_id=order.id,payment_method=method,amount=order.total_amount)       
        f = Feedback(customer_id = current_user.id,order_id=order.id,rating =rating,comment=feedback) 
        order.status = 'sending'
        db.session.add(a)
        db.session.add(f)
        db.session.add(p)
        db.session.commit()
        flash("The order was placed", 'success')
        return redirect (url_for('shop.dashboard'))
    
    
    
    
@blueprint.route('/dashboard', methods=["GET","POST"])
@login_required
def dashboard():
    context = {}
    context['orders'] = current_user.orders
    if request.method=="GET":
        return render_template('dashboard.html',**context)
    
    if request.method=="POST":
        username = request.form.get('username',"").strip()
        password = request.form.get('password',"").strip()
        email = request.form.get('email',"").strip()

        current_user.username = username
        current_user.email = email
        if password:
            current_user.password = password
        db.session.commit()
        return render_template('dashboard.html',**context)
    
    


