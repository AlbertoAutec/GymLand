# Logica per operazioni trainer
class TrainerController:
    def crea_scheda(self, trainer_id, dati_scheda):
        # Crea una nuova scheda per un utente
        from models.scheda import SchedaModel
        scheda = SchedaModel(
            user_id=dati_scheda["user_id"],
            trainer_id=trainer_id,
            validita_inizio=dati_scheda.get("validita_inizio"),
            validita_fine=dati_scheda.get("validita_fine"),
            descrizione=dati_scheda.get("descrizione")
        )
        # Aggiungi esercizi se presenti
        if "esercizi" in dati_scheda:
            scheda.esercizi = dati_scheda["esercizi"]
        from db import db
        db.session.add(scheda)
        db.session.commit()
        return scheda
    def crud_esercizi(self, trainer_id, dati_esercizio):
        # Esempio: crea o aggiorna esercizio
        from models.esercizio import EsercizioModel
        from db import db
        esercizio = EsercizioModel.query.filter_by(id=dati_esercizio.get("id")).first()
        if esercizio:
            esercizio.nome = dati_esercizio.get("nome", esercizio.nome)
            esercizio.descrizione = dati_esercizio.get("descrizione", esercizio.descrizione)
            esercizio.immagine = dati_esercizio.get("immagine", esercizio.immagine)
        else:
            esercizio = EsercizioModel(**dati_esercizio)
            db.session.add(esercizio)
        db.session.commit()
        return esercizio
