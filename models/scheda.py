from db import db
from .user import UserModel
from .trainer import TrainerModel
from .esercizio import EsercizioModel

scheda_esercizi = db.Table(
    'scheda_esercizi',
    db.Column('scheda_id', db.Integer, db.ForeignKey('schede.id')),
    db.Column('esercizio_id', db.Integer, db.ForeignKey('esercizi.id'))
)

class SchedaModel(db.Model):
    __tablename__ = "schede"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    validita_inizio = db.Column(db.Date)
    validita_fine = db.Column(db.Date)
    esercizi = db.relationship('EsercizioModel', secondary=scheda_esercizi, backref='schede')
    # ...eventuali altri campi...