from flask_sqlalchemy import SQLAlchemy
from db import db
from .user import UserModel

class TrainerModel(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel', backref='trainer_profile')

    # Add any additional fields for the Trainer model here
    # For example:
    # specialization = db.Column(db.String(100))
    # experience_years = db.Column(db.Integer)

    def __repr__(self):
        return f'<Trainer {self.id}>'