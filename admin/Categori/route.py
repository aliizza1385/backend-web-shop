import os
from flask import Blueprint, jsonify, request
from .models import Categori
from initialize import db


blueprint = Blueprint('categori', __name__)



@blueprint.route('/categori', methods=["GET"])
def product():
    c = Categori.query.all()
    categori = []
    for categor in c:
        categori.append({
            'id':c.id,
            'name':c.name,
            'description':c.category_id,
            'parent_category_id':c.description,
            'created_at':c.price,
            
        })

    response = jsonify(c)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(c)
    return response


# @blueprint.route('/product', methods=["POST"])
# def product_create():
#     # Get information at form
#     name = request.form.get('name', "").strip()
#     description = request.form.get('description', "").strip()
#     price = request.form.get('price', "").strip()
#     category_id = int(request.form.get('category_id', "").strip())
#     imagefile = request.files.get('image')
#     filename = imagefile.filename

#     if imagefile:
#         imagefile.save(os.path.join(UPLOAD_FOLDER, filename))
#         product = Product(name =name,description =description,price = price,category_id = category_id,image=filename)
#     else:
#         product = Product(name =name,description =description,price = price,category_id = category_id)

#     db.session.add(product)
#     db.session.commit()
#     return jsonify({
#             'category_id':product.category_id,
#             'id':product.id,
#             'name':product.name,
#             'description':product.description,
#             'price':product.price,
#             'image':product.image
#         })
    
    
# @blueprint.route('/product/<int:id>', methods=["DELETE"])
# def DELETE_one_product(id):
#     product = Product.query.get_or_404(id)
#     db.session.delete(product)
#     db.session.commit()
#     product = {
#         "id": product.id,
#         'name': product.name,
#         'description': product.description,
#         'price': product.price,
#         'image':product.image
#     }
#     return jsonify(product)


# @blueprint.route('/product/<int:id>', methods=["GET"])
# def show_one_product(id):
#     one_product = Product.query.get_or_404(id)
#     if one_product is None:
#         return '', 404
#     return jsonify({
#         "id":id,
#         'name':one_product.name,
#         'description':one_product.description,
#         'price':one_product.price,
#         'image':one_product.image
#     })



# @blueprint.route('/product/<int:id>', methods=["PUT"])
# def update_product(id):
#     # Check if product exists
#     product_want_update = Product.query.get_or_404(id)

    
#     # Update product data
#     name = request.form.get('name', "").strip()
#     description = request.form.get('description', "").strip()
#     price = request.form.get('price', "").strip()
#     category_id = request.form.get('category_id', "").strip()
#     image = request.files.get('image')  
#     filename = image.filename
    
#     # Update product data if provided
#     if name and description and price:
#         if image:
#             image.save(os.path.join(UPLOAD_FOLDER, filename))
#             product = Product(name =name,description =description,price = price,category_id = category_id,image=filename)
#         else:
#             product = Product(name =name,description =description,price = price,category_id = category_id)
#     # put information
#     product_want_update.name = product.name
#     product_want_update.description = product.description
#     product_want_update.price = product.price
#     product_want_update.category_id = product.category_id
#     product_want_update.image = filename
    
#     db.session.commit()
#     return jsonify({
#         "id":id,
#         'name':product_want_update.name,
#         'description':product_want_update.description,
#         'price':product_want_update.price,
#         'image':product_want_update.image
#     })