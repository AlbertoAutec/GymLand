from flask_sqlalchemy import SQLAlchemy
from db import db
from .user import UserModel

class TrainerModel(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel', backref='trainer_profile')

    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)

    # Relazione con le schede
    schede = db.relationship('SchedaModel', backref='trainer', lazy='dynamic')

    def __repr__(self):
        return f'<Trainer {self.id}>'