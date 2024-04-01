from flask import Blueprint, jsonify, request
from .models import User
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
from admin.Logs.route import get_log_and_save_then


blueprint = Blueprint('user', __name__)




@blueprint.route('/users/<int:id>', methods=["DELETE"])
def DELETE_one_user(id):
    print('ali')
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    # get id admin to want to do work and ip then
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Delete User: {id}', Ip_address )
    user = {
        "id": user.id,
        'username': user.username,
        'password_hash': user.password_hash,
        'email': user.email,
    }
    return jsonify(user)


@blueprint.route('/users', methods=["GET"])
def users():
    users = User.query.all()
    all_users = []
    for user in users:
        all_users.append({
            "id":user.id,
            'username':user.username,
            'password_hash':user.password_hash,
            'email':user.email,
        })
    response = jsonify(all_users)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_users)
    return response


@blueprint.route('/users/<int:id>', methods=["GET"])
def show_one_user(id):
    one_user = User.query.get_or_404(id)
    if one_user is None:
        return '', 404
    return jsonify({
        "id":one_user.id,
        'username': one_user.username,
        'password': one_user.password_hash,
        'email': one_user.email,

    })


@blueprint.route('/users/<int:id>', methods=["PUT"])
def update_user(id):
    # Check if user exists
    user_want_update = User.query.get_or_404(id)
    
    # Get all data from db
    all_data = User.query.all()
    
    
    # Update user data
    username = request.json.get('username', "").strip()
    password_hash = request.json.get('password', "").strip()
    email = request.json.get('email', "").strip()
    
    # check username and password_hash unic
    for i in all_data:
        if i.id != id and i.username == username:
            username = username + '_copy'
    for i in all_data:
        if i.id != id and i.password_hash == password_hash:
            password_hash =  'copy_' + password_hash 
    
    # Update user data if provided
    user_want_update.username = username
    user_want_update.password_hash = password_hash
    user_want_update.email = email
    
    db.session.commit()
    
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Update User: {user_want_update.id}', Ip_address )
        
    return jsonify({
        "id":id,
        'username':user_want_update.username,
        'password_hash':user_want_update.password_hash,
        'email':user_want_update.email,
    })

    
    
@blueprint.route('/user_creaete', methods=["POST"])
def create_user():
    # Get the user input from the request body
    username = request.json.get('username', "").strip()
    password_hash = request.json.get('password_hash', "").strip()
    email = request.json.get('email', "").strip()
    password_hash = request.json.get('password', "").strip()
    # password_hash = bcrypt.generate_password_hash(password_hash).decode('utf-8')

    # Get all user in db
    All_db_user = User.query.all()
    
    # check this user have or not
    have_or_not_username = User.query.filter_by(username = username).first()
    have_or_not_email = User.query.filter_by(email = email).first()
    
    if have_or_not_username:
        username = username + '_copy'
    if have_or_not_email:
        email =  ' copy_' + email

    # Create a new user and save it to the database
    new_user = User(username=username, password_hash=password_hash, email=email)
    db.session.add(new_user)
    db.session.commit()
    # get id admin to want to do work and ip then
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Create User: {new_user.id}', Ip_address )
    # Return a success message
    return jsonify({
        "id": new_user.id,
        'username': new_user.username,
        'password_hash': new_user.password_hash,
        'email': new_user.email,
    })



@blueprint.route('/admin/login', methods=["POST","GET"])
def login_one_user(id):
    username = request.json.get('username', "").strip()
    password = request.json.get('password', "").strip()
    user = User.query.filter(username = username).first()
    
    if user.password == password:
        user = {
            "id": user.id,
            'username': user.username,
            'password': user.password,
            'email': user.email,
        }
        return jsonify(user)

