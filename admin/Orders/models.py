from initialize import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), nullable=False)

    address = db.relationship("Address", backref="order",cascade='all, delete-orphan', lazy=True)
    orderitems = db.relationship("OrderItem", backref="order",cascade='all, delete-orphan', lazy=True)
    payments = db.relationship("Payment", backref="order",cascade='all, delete-orphan', lazy=True)
    feedbacks = db.relationship("Feedback", backref="order",cascade='all, delete-orphan', lazy=True)

    @property
    def total_amount(self):
        All = 0
        for orderitem in self.orderitems:
            price = orderitem.product.price
            quantity = orderitem.quantity
            All += price * quantity
        return All


    def __repr__(self):
        return '<order %r>' % self.id