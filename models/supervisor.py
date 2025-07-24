from flask_sqlalchemy import SQLAlchemy
from .user import User, db

class Supervisor(db.Model):
    __tablename__ = 'supervisors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='supervisor_profile')

    # Add any additional fields or methods for the Supervisor model here