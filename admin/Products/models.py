from initialize import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    orderitems = db.relationship("OrderItem", backref="product",cascade='all, delete-orphan', lazy=True)
    
    def __repr__(self):
        return '<Product %r>' % self.id
