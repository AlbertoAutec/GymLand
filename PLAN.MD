# 📌 Piano di sviluppo GymLand
> Aggiorna spuntando le attività completate.

## ✅ Setup iniziale
- [x] Creare repo Git/GitHub
- [x] Copiare scheletro progetto (Flask REST API)
- [x] Creare ambiente virtuale e installare requirements
- [x] Configurare VSCode (debug, Copilot, ecc.)

## ✅ Database e Modelli (SQLAlchemy + SQLite)
- [ ] Definire modello Utente (USER) con dati personali e abbonamento
- [ ] Definire modello Trainer
- [ ] Definire modello Supervisore (ruolo in tabella Users con flag)
- [ ] Definire modello Esercizio (nome, descrizione, immagine)
- [ ] Definire modello Scheda (relazione User-Trainer, lista esercizi, validità)
- [ ] Migrazioni iniziali con Flask-Migrate

## ✅ Autenticazione e Autorizzazioni
- [ ] Implementare JWT (login, refresh, logout, registrazione)
- [ ] Proteggere endpoint secondo ruolo (decoratori)
- [ ] Testare con Postman/Insomnia

## ✅ Struttura MVC
- [ ] Creare cartella `models` con i file SQLAlchemy
- [ ] Creare cartella `controllers` per le logiche dei vari ruoli
- [ ] Creare cartella `views` per i template HTML (Flask render_template)
- [ ] Integrare Bootstrap o Tailwind per frontend responsive
- [ ] Implementare rotte Flask che richiamano i controller

## ✅ Funzionalità USER
- [ ] Dashboard utente con scheda allenamento attiva
- [ ] Funzione per segnare esercizio completato
- [ ] Calendario attività personali

## ✅ Funzionalità TRAINER
- [ ] CRUD esercizi (con upload immagine)
- [ ] Creazione e assegnazione schede a utenti
- [ ] Generazione schede fittizie

## ✅ Funzionalità SUPERVISOR
- [ ] Dashboard supervisore con statistiche
- [ ] Gestione utenti e trainer (CRUD)
- [ ] Revisione schede e esercizi

## ✅ Test e Deployment
- [ ] Scrivere test unitari e d’integrazione
- [ ] Dockerizzare (basato sul tuo Dockerfile)
- [ ] Aggiornare `docker-compose.yml` per SQLite o Postgres
- [ ] Deployment su server o container cloud
