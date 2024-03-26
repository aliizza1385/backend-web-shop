from initialize import db
from datetime import datetime


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    recipient_name = db.Column(db.String(60), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return '<Address %r>' % self.id