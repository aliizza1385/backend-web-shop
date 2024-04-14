from initialize import db
from datetime import datetime

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<OrderItem %r>' % self.id
