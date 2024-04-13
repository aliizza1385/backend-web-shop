from flask import Blueprint, render_template, request, flash, redirect, url_for
# from flask_login import login_user, current_user, logout_user, login_required
from initialize import db
from config import UPLOAD_FOLDER, localhost

# Create a Blueprint named 'login'
blueprint = Blueprint('custoemr', __name__)


@blueprint.route('/custoemr/proile')
def profile_customer():
    # print(current_user.username)
    return render_template('profile_customer.html')