# Logica per operazioni utente
class UserController:
    def get_dashboard(self, user_id):
        # Restituisce la scheda attiva e il calendario degli esercizi completati
        from models.user import UserModel
        from models.scheda import SchedaModel
        user = UserModel.query.get(user_id)
        if not user:
            return None
        scheda_attiva = SchedaModel.query.filter_by(user_id=user_id).order_by(SchedaModel.validita_inizio.desc()).first()
        calendario = []  # Qui puoi implementare la logica per il calendario attività
        return {
            "scheda_attiva": scheda_attiva,
            "calendario": calendario
        }
    def segna_esercizio_completato(self, user_id, esercizio_id):
        # Segna l'esercizio come completato per l'utente (logica semplificata)
        # Qui si potrebbe aggiungere una tabella di tracking esercizi completati
        # Esempio: EsercizioCompletato(user_id=user_id, esercizio_id=esercizio_id, data=oggi)
        return True
