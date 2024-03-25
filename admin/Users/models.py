from initialize import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    logs = db.relationship("Logs", backref="user",cascade='all, delete-orphan', lazy=True)
    
    
    
    def __repr__(self):
        return '<User %r>' % self.id
 