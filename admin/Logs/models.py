from initialize import db
from datetime import datetime


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    action_date = db.Column(db.DateTime, default=datetime.now)
    ip_address = db.Column(db.String(50), nullable=False)
    
    
    def __repr__(self):
        return '<Logs %r>' % self.id