# 📌 Piano di sviluppo GymLand
> Aggiorna spuntando le attività completate.

## ✅ Setup iniziale
- [x] Creare repo Git/GitHub
- [x] Copiare scheletro progetto (Flask REST API)
- [x] Creare ambiente virtuale e installare requirements
- [x] Configurare VSCode (debug, Copilot, ecc.)

## ✅ Database e Modelli (SQLAlchemy + SQLite)
 - [x] Definire modello Utente (USER) con dati personali e abbonamento
 - [x] Definire modello Trainer
 - [x] Definire modello Supervisore (ruolo in tabella Users con flag)
 - [x] Definire modello Esercizio (nome, descrizione, immagine)
 - [x] Definire modello Scheda (relazione User-Trainer, lista esercizi, validità)
 - [x] Migrazioni iniziali con Flask-Migrate

## ✅ Autenticazione e Autorizzazioni
 - [x] Implementare JWT (login, refresh, logout, registrazione)
 - [x] Proteggere endpoint secondo ruolo (decoratori)
- [ ] Testare con Postman/Insomnia

## ✅ Struttura MVC
- [x] Creare cartella `models` con i file SQLAlchemy
- [x] Creare cartella `controllers` per le logiche dei vari ruoli
- [x] Creare cartella `views` per i template HTML (Flask render_template)
- [x] Integrare Bootstrap o Tailwind per frontend responsive
- [x] Implementare rotte Flask che richiamano i controller

## ✅ Funzionalità USER
- [x] Dashboard utente con scheda allenamento attiva
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
