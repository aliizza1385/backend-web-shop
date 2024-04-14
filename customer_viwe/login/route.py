from flask import Blueprint, render_template, request, flash, redirect, url_for
from admin.Customers.models import Customer
from initialize import db
from flask_login import current_user,login_user,login_required,logout_user

# Create a Blueprint named 'login'
blueprint = Blueprint('login', __name__)

# Define the route for login with both GET and POST methods
# @blueprint.route('/home', methods=["GET", "POST"])
# @login_required
# def home():
    # return render_template('index.html')

@blueprint.route('/shop')
# @login_required
def shop():
    return render_template('shop.html')


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('login.shop'))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pass']
        customer = Customer.query.filter_by(email = email).first()
        if customer and customer.password == password: 
            login_user(customer ,remember=True)
            flash('You were successfully logged in','success')
            return redirect(url_for('login.shop'))
        else:
            flash('Email or password wrong','danger')
            return redirect(url_for('login.login'))
    else:
        return render_template('customer_login.html')
    
@blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('shop.shop'))


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    # if form.valid
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        phone_number = request.form['phone_number']
        email_already = Customer.query.filter_by(email = email).first()
        username_already = Customer.query.filter_by(username = username).first()
        
        if email_already and username_already:
            flash('Customer already exists','danger')
            return redirect(url_for('login.register'))
        else:
            new_customer = Customer(username = username, email = email, password = password, phone_number = phone_number)
            flash('Customer Created','success')
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('login.shop'))

    else:
        return render_template('register.html')

