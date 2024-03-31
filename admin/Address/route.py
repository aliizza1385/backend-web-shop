from flask import Blueprint, jsonify, request
from .models import Address
from flask_bcrypt import generate_password_hash
from werkzeug.exceptions import BadRequest
from initialize import db
from admin.Logs.route import get_log_and_save_then


blueprint = Blueprint('address', __name__)

    

@blueprint.route('/address', methods=["GET"])
def address():
    address = Address.query.all()
    all_address = []
    for address_in_for in address:
        all_address.append({
        "id": address_in_for.id,
        'customer_id': address_in_for.customer.username,
        'recipient_name': address_in_for.recipient_name,
        'address_line1': address_in_for.address_line1,
        'address_line2': address_in_for.address_line2,
        'city': address_in_for.city,
        'state': address_in_for.state,
        'postal_code': address_in_for.postal_code,
        'country': address_in_for.country,
        })
    response = jsonify(all_address)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_address)
    return response


@blueprint.route('/address/<int:id>', methods=["GET"])
def show_one_address(id):
    one_address = Address.query.get_or_404(id)
    if one_address is None:
        return '', 404
    return jsonify({
        "id": one_address.id,
        'customer_id': one_address.customer_id,
        'recipient_name': one_address.recipient_name,
        'address_line1': one_address.address_line1,
        'address_line2': one_address.address_line2,
        'city': one_address.city,
        'state': one_address.state,
        'postal_code': one_address.postal_code,
        'country': one_address.country,
    })



@blueprint.route('/address/<int:id>', methods=["PUT"])
def address_update(id):
    # Check if address exists
    address_want_update = Address.query.get_or_404(id)

    
    # Update address data
    address_want_update.recipient_name = request.json.get('recipient_name', "").strip()
    address_want_update.address_line1 = request.json.get('address_line1', "").strip()
    address_want_update.address_line2 = request.json.get('address_line2', "").strip()
    address_want_update.city = request.json.get('city', "").strip()
    address_want_update.state = request.json.get('state', "").strip()
    address_want_update.postal_code = request.json.get('postal_code', "").strip()
    
    db.session.commit()
    
    # get id admin to want to do work and ip then
    user_id = request.headers.get("user")
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Update Address: {id}', user_id, Ip_address )
    
    
    return jsonify({
        "id": address_want_update.id,
        'customer_id': address_want_update.customer_id,
        'recipient_name': address_want_update.recipient_name,
        'address_line1': address_want_update.address_line1,
        'address_line2': address_want_update.address_line2,
        'city': address_want_update.city,
        'state': address_want_update.state,
        'postal_code': address_want_update.postal_code,
        'country': address_want_update.country,
    })




@blueprint.route('/address/<int:id>', methods=["DELETE"])
def DELETE_one_address(id):
    address = Address.query.get_or_404(id)
    db.session.delete(address)
    db.session.commit()
    
    # get id admin to want to do work and ip then
    
    user_id = request.headers.get("user")
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Delete Address: {id}', user_id, Ip_address )
    address = {
        "id": address.id,
        'customer_id': address.customer_id,
        'recipient_name': address.recipient_name,
        'address_line1': address.address_line1,
        'address_line2': address.address_line2,
        'city': address.city,
        'state': address.state,
        'postal_code': address.postal_code,
        'country': address.country,
    }
    return jsonify(address)
    