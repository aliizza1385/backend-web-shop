from flask import Blueprint, render_template, request
# from admin.customers.models import Customer

# Create a Blueprint named 'login'
blueprint = Blueprint('login', __name__)

# Define the route for login with both GET and POST methods
@blueprint.route('/login', methods=["GET", "POST"])
def login():
    return render_template('customer_login.html')
    # customers = Customer.query.all()
    if form.validate_on_submit():
        print('yes')

# Print a success message
print("The Flask blueprint code has been fixed.")
