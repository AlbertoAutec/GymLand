from db import db  #qui importiamo il database dal file db.py

class UserModel(db.Model):  #qui definiamo il modello UserModel che rappresenta gli utenti nel database
    __tablename__ = "users"  #qui definiamo il nome della tabella nel database

    id = db.Column(db.Integer, primary_key=True)  #qui definiamo la colonna id come chiave primaria
    nome = db.Column(db.String(50), nullable=False)  #qui definiamo la colonna nome come stringa non nulla
    cognome = db.Column(db.String(50), nullable=False)  #qui definiamo la colonna cognome come stringa non nulla
    indirizzo = db.Column(db.String(200))  #qui definiamo la colonna indirizzo come stringa
    password = db.Column(db.String(200), nullable=False)  #qui definiamo la colonna password come stringa non nulla
    abbonamento_inizio = db.Column(db.Date)  #qui definiamo la colonna abbonamento_inizio come data
    abbonamento_fine = db.Column(db.Date)  #qui definiamo la colonna abbonamento_fine come data
    ruolo = db.Column(db.String(20), nullable=False)  #qui definiamo la colonna ruolo come stringa non nulla, i valori possono essere 'user', 'trainer' o 'supervisor'
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email unica e obbligatoria

    # Relazione con le schede
    schede = db.relationship('SchedaModel', backref='utente', lazy='dynamic')

    def abbonamento_attivo(self):
        """Restituisce True se l'abbonamento è attivo oggi."""
        from datetime import date
        oggi = date.today()
        return (self.abbonamento_inizio is None or self.abbonamento_inizio <= oggi) and \
               (self.abbonamento_fine is None or self.abbonamento_fine >= oggi)

    def __repr__(self):  #qui definiamo il metodo di rappresentazione dell'oggetto UserModel
        return f"<User {self.nome} {self.cognome}>"  #restituiamo una stringa che rappresenta l'utente
