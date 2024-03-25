from initialize import db
from datetime import datetime


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Feedback %r>' % self.id