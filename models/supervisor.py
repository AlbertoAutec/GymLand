from .user import UserModel, db

class SupervisorModel(db.Model):
    __tablename__ = 'supervisors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel', backref='supervisor_profile')
    attivo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Supervisor id={self.id} user_id={self.user_id} attivo={self.attivo}>"

    def statistiche_utenti(self):
        pass