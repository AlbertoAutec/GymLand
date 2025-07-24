from flask_sqlalchemy import SQLAlchemy
from .user import User, db

class Supervisor(db.Model):
    __tablename__ = 'supervisors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='supervisor_profile')

    # Flag per ruolo supervisor (può essere gestito anche in User)
    attivo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Supervisor id={self.id} user_id={self.user_id} attivo={self.attivo}>"

    def statistiche_utenti(self):
        # Placeholder: qui si potrebbero calcolare statistiche sugli utenti
        pass