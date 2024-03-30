from flask import Blueprint, request, jsonify
from admin.Users.models import User

blueprint = Blueprint('login_admin', __name__)



@blueprint.route('/login',methods=["POST"])
def login():
    
    username = request.json.get('username').strip()
    password = request.json.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if username == 'alireza' and password == 'hosseini':
        return jsonify({
            'id':0,
            'username':'alireza',
        }) 
    elif user and user.password_hash == password:
        return jsonify({
            'id':user.id,
            'username':user.username,
            })
    return ({"message":"username or password error"}) , 404