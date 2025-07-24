# Logica per operazioni supervisor
class SupervisorController:
    def dashboard(self):
        # Restituisce statistiche generali
        from models.user import UserModel
        from models.trainer import TrainerModel
        from models.scheda import SchedaModel
        utenti_totali = UserModel.query.count()
        abbonamenti_attivi = UserModel.query.filter(UserModel.abbonamento_fine >= 'today').count()  # semplificato
        schede_per_trainer = {}  # Puoi popolare con una query
        return {
            "utenti_totali": utenti_totali,
            "abbonamenti_attivi": abbonamenti_attivi,
            "schede_per_trainer": schede_per_trainer
        }
    def gestisci_utenti_trainer(self):
        # Esempio: restituisce lista utenti e trainer
        from models.user import UserModel
        from models.trainer import TrainerModel
        utenti = UserModel.query.all()
        trainer = TrainerModel.query.all()
        return {"utenti": utenti, "trainer": trainer}
    def revisione_schede_esercizi(self):
        # Esempio: restituisce tutte le schede ed esercizi
        from models.scheda import SchedaModel
        from models.esercizio import EsercizioModel
        schede = SchedaModel.query.all()
        esercizi = EsercizioModel.query.all()
        return {"schede": schede, "esercizi": esercizi}
