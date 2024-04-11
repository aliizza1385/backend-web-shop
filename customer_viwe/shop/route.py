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

