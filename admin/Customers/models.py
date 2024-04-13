from initialize import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def get_user(customer_id):
    return Customer.query.get(customer_id)



# UserMixin
class Customer(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # password = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    orders = db.relationship('Order',cascade='all, delete-orphan', backref='customer')
    feedbacks = db.relationship('Feedback',cascade='all, delete-orphan', backref='customer', lazy=True)
    address = db.relationship('Address',cascade='all, delete-orphan', backref='customer', lazy=True)
    
    def __repr__(self):
        return '<Customer %r>' % self.username
    
    
    