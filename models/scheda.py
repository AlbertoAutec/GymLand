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
    descrizione = db.Column(db.String(255))  # campo opzionale per note o descrizione

    def is_attiva(self):
        """Restituisce True se la scheda è attualmente valida."""
        from datetime import date
        oggi = date.today()
        return (self.validita_inizio is None or self.validita_inizio <= oggi) and \
               (self.validita_fine is None or self.validita_fine >= oggi)

    def aggiungi_esercizio(self, esercizio):
        """Aggiunge un esercizio alla scheda se non già presente."""
        if esercizio not in self.esercizi:
            self.esercizi.append(esercizio)

    def rimuovi_esercizio(self, esercizio):
        """Rimuove un esercizio dalla scheda se presente."""
        if esercizio in self.esercizi:
            self.esercizi.remove(esercizio)

    def __repr__(self):
        return f"<Scheda id={self.id} user_id={self.user_id} trainer_id={self.trainer_id} attiva={self.is_attiva()}>"