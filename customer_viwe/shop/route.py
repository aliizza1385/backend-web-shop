from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from initialize import db
from admin.Categori.models import Category
from admin.Products.models import Product
from config import UPLOAD_FOLDER, localhost

# Create a Blueprint named 'login'
blueprint = Blueprint('shop', __name__)


@blueprint.route('/shop')
def shop():
    categories = Category.query.all()
    products = Product.query.all()
            
    return render_template('shop.html', categories = categories,products=products)

@blueprint.route('/<int:id>')
def category_by_id(id):
    categories = Category.query.all()
    products = Product.query.filter(Product.category_id == id)

    return render_template('shop.html', categories = categories,products=products)


@blueprint.route('/detail/<int:product_id>')
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)

    return render_template('product-details.html', product = product)

@blueprint.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    quantity = request.form.get('quantity')
    # return 'Product added to cart'

    return render_template('shop-cart.html')

