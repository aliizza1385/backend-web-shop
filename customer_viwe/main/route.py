from flask import Flask,jsonify, render_template,Blueprint
from initialize import db

blueprint = Blueprint('main', __name__)



@blueprint.route('/main')
def home():
    return render_template('main.html')