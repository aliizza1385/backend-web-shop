from flask import Blueprint, jsonify, request
from .models import Customer
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
from admin.Logs.route import get_log_and_save_then


blueprint = Blueprint('customer', __name__)

def get_customer(id):
    customer_want_update = Customer.query.get_or_404(id)
    final_customer = {
        "id": customer_want_update.id,
        "username": customer_want_update.username,
        "email": customer_want_update.email,
        "phone": customer_want_update.phone_number,
        "registration_date": customer_want_update.registration_date,
        "password": customer_want_update.password,
    }
    return final_customer
    


@blueprint.route('/customers', methods=["GET"])
def customers():
    customers = Customer.query.all()
    all_customers = []
    for customer_in_for in customers:
        all_customers.append({
            "id":customer_in_for.id,
            'username':customer_in_for.username,
            'email':customer_in_for.email,
            'phone_number':customer_in_for.phone_number,
            'registration_date':customer_in_for.registration_date,
        })

    response = jsonify(all_customers)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_customers)
    return response


@blueprint.route('/customers/<int:id>', methods=["GET"])
def show_one_customer(id):
    one_customer = Customer.query.get_or_404(id)
    if one_customer is None:
        return '', 404
    return jsonify({
        "id":one_customer.id,
        'username': one_customer.username,
        'email': one_customer.email,
        'phone_number': one_customer.phone_number,
        'registration_date': one_customer.registration_date,
        'password': one_customer.password,
    })



@blueprint.route('/customers/<int:id>', methods=["PUT"])
def update_customer(id):
    # Check if customer exists
    customer_want_update = Customer.query.get_or_404(id)
    
    # Get all data from db
    all_data = Customer.query.all()
    
    # Get data from request
    data = request.get_json()
    
    
    # Update customer data
    username = request.json.get('username', "").strip()
    email = request.json.get('email', "").strip()
    phone_number = request.json.get('phone_number', "").strip()
    password = request.json.get('password', "").strip()
    
    
    
    # check username and email unic
    for i in all_data:
        if i.id != id and i.username == username:
            username = username + '_copy'
    for i in all_data:
        if i.id != id and i.email == email:
            email =  'copy_' + email 

    
    
    # Update customer data if provided
    if username:
        customer_want_update.username = username
    if email:
        customer_want_update.email = email
    if phone_number:
        customer_want_update.phone_number = phone_number
    if password:
        customer_want_update.password = password
        
        
        
    # get id admin to want to do work
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Update Customer {customer_want_update.id}', Ip_address )
    
    
    db.session.commit()
    return jsonify({
        "id":id,
        'username':customer_want_update.username,
        'email':customer_want_update.email,
        'phone_number':customer_want_update.phone_number,
        'password':customer_want_update.password,
    })

    
    
@blueprint.route('/customer_creaete', methods=["POST"])
def create_customer():
    # Get the user input from the request body
    username = request.json.get('username', "").strip()
    email = request.json.get('email', "").strip()
    phone_number = request.json.get('phone_number', "").strip()
    password = request.json.get('password', "").strip()

    # Get all user in db
    All_db_customer = Customer.query.all()
    
    # check this customer have or not
    have_or_not_username = Customer.query.filter_by(username = username).first()
    have_or_not_email = Customer.query.filter_by(email = email).first()
    


    if have_or_not_username:
        username = username + '_copy'
    if have_or_not_email:
        email = 'copy_' + email


    # Create a new user and save it to the database
    new_user = Customer(username=username, email=email, phone_number=phone_number,password = password)
    db.session.add(new_user)
    db.session.commit()
    
    
    # get id admin to want to do work and ip then
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Create Customer: {new_user.id}', Ip_address )

    # Return a success message
    return jsonify({
        "id": new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'phone_number': new_user.phone_number,
        'password': new_user.password,
    })



@blueprint.route('/customers/<int:id>', methods=["DELETE"])
def DELETE_one_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    
    # get id admin to want to do work and ip then
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Delete Customer: {id}', Ip_address )
    
    customer = {
        "id": customer.id,
        'username': customer.username,
        'email': customer.email,
        'phone_number': customer.phone_number,
    }
    return jsonify(customer)
