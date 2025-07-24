from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Esercizio(db.Model):
    __tablename__ = 'esercizi'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    immagine = db.Column(db.String(200))