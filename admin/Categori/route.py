from flask import Blueprint, jsonify, request
from .models import Category
from initialize import db
from admin.Logs.route import get_log_and_save_then



blueprint = Blueprint('category', __name__)


# this for Show list category

@blueprint.route('/category', methods=["GET"])
def category():
    c = Category.query.all()
    category = []
    for categor in c:
        category.append({
            'id':categor.id,
            'name':categor.name,
            'description':categor.description,
            'parent_category_id':categor.parent_category_id,
            'created_at':categor.created_at,
            
        })

    response = jsonify(category)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(category)
    return response


# this for create category

@blueprint.route('/category', methods=["POST"])
def category_create():
    # Get information at form
    name = request.json.get('name', "").strip()
    description = request.json.get('description', "").strip()
    parent_category_id = request.json.get('parent_category_id', "").strip()

    New_category = Category(name =name,description =description,parent_category_id = parent_category_id)

    db.session.add(New_category)
    db.session.commit()
   # get id admin to want to do work and ip then
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Create category: {New_category.id}', Ip_address )
    
    
    return jsonify({
            'id':New_category.id,
            'name':New_category.name,
            'description':New_category.description,
            'parent_category_id':New_category.parent_category_id,
        })


    
# this for DELETE_category

@blueprint.route('/category/<int:id>', methods=["DELETE"])
def DELETE_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    
    # get id admin to want to do work and ip then
    user_id = request.headers.get("user")
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Delete category: {id}', user_id, Ip_address )
    
    category = {
        "id": category.id,
        'name': category.name,
        'description': category.description,
        'parent_category_id': category.parent_category_id,
    }
    return jsonify(category)



# this for show one category

@blueprint.route('/category/<int:id>', methods=["GET"])
def show_one_category(id):
    one_categoryt = Category.query.get_or_404(id)
    if one_categoryt is None:
        return '', 404
    return jsonify({
        "id":id,
        'name':one_categoryt.name,
        'description':one_categoryt.description,
        'parent_category_id':one_categoryt.parent_category_id,
    })



# this for update category

@blueprint.route('/category/<int:id>', methods=["PUT"])
def update_category(id):
    # Check if category exists
    category_want_update = Category.query.get_or_404(id)

    
    # Update category data
    name = request.json.get('name', "").strip()
    description = request.json.get('description', "").strip()
    parent_category_id = request.json.get('parent_category_id', "").strip()
    
    # Update category data if provided
    if name:
        category_want_update.name = name 
    if description:
        category_want_update.description = description
    if parent_category_id:
        category_want_update.parent_category_id = parent_category_id

    db.session.commit()
    
    # get id admin to want to do work and ip then
    user_id = request.headers.get("user")
    Ip_address = request.remote_addr
    get_log_and_save_then(f'Update category: {id}', user_id, Ip_address )
    
    
    return jsonify({
        "id":id,
        'name':category_want_update.name,
        'description':category_want_update.description,
        'parent_category_id':category_want_update.parent_category_id,
    })