from initialize import db
from datetime import datetime






class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    # password = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)

    orders = db.relationship('Order', backref='customer')
    feedbacks = db.relationship('Feedback', backref='customer', lazy=True)
    address = db.relationship('Address', backref='customer', lazy=True)
    