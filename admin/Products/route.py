import os
from flask import Blueprint, jsonify, request,url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from .models import Product
from initialize import db
from config import UPLOAD_FOLDER

blueprint = Blueprint('product', __name__)




@blueprint.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    return send_from_directory(UPLOAD_FOLDER, filename)


@blueprint.route('/product', methods=["GET"])
def product():
    products = Product.query.all()
    all_product = []
    for product in products:
        all_product.append({
            'id':product.id,
            'name':product.name,
            'category_id':product.category_id,
            'description':product.description,
            'price':product.price,
            'image' : 'http://localhost:5000/'+'uploads/'+ product.image
            
        })


    response = jsonify(all_product)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(all_product)
    return response


@blueprint.route('/product', methods=["POST"])
def product_create():
    # Get information at form
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    category_id = int(request.form.get('category_id', "").strip())
    imagefile = request.files.get('image')
    filename = imagefile.filename

    if imagefile:
        imagefile.save(os.path.join(UPLOAD_FOLDER, filename))
        product = Product(name =name,description =description,price = price,category_id = category_id,image=filename)
    else:
        product = Product(name =name,description =description,price = price,category_id = category_id)

    db.session.add(product)
    db.session.commit()
    return jsonify({
            'category_id':product.category_id,
            'id':product.id,
            'name':product.name,
            'description':product.description,
            'price':product.price,
            'image':product.image
        })
    
    
@blueprint.route('/product/<int:id>', methods=["DELETE"])
def DELETE_one_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    product = {
        "id": product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image':product.image
    }
    return jsonify(product)


@blueprint.route('/product/<int:id>', methods=["GET"])
def show_one_product(id):
    one_product = Product.query.get_or_404(id)
    if one_product is None:
        return '', 404
    return jsonify({
        "id":id,
        'name':one_product.name,
        'description':one_product.description,
        'price':one_product.price,
        'image':one_product.image
    })



@blueprint.route('/product/<int:id>', methods=["PUT"])
def update_product(id):
    # Check if product exists
    product_want_update = Product.query.get_or_404(id)

    
    # Update product data
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    category_id = request.form.get('category_id', "").strip()
    image = request.files.get('image')  
    filename = image.filename
    
    # Update product data if provided
    if name and description and price:
        if image:
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            product = Product(name =name,description =description,price = price,category_id = category_id,image=filename)
        else:
            product = Product(name =name,description =description,price = price,category_id = category_id)
    # put information
    product_want_update.name = product.name
    product_want_update.description = product.description
    product_want_update.price = product.price
    product_want_update.category_id = product.category_id
    product_want_update.image = filename
    
    db.session.commit()
    return jsonify({
        "id":id,
        'name':product_want_update.name,
        'description':product_want_update.description,
        'price':product_want_update.price,
        'image':product_want_update.image
    })