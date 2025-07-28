from db import db

class EsercizioModel(db.Model):
    __tablename__ = 'esercizi'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text)
    immagine = db.Column(db.String(200))

    def __repr__(self):
        return f"<Esercizio id={self.id} nome={self.nome}>"

    def has_image(self):
        return bool(self.immagine)