# GymLand REST API + MVC WebApp

Questa è una webapp/REST API sviluppata in Python 3.10 con **Flask**, **SQLAlchemy** (SQLite), e architettura **MVC**, per la gestione di una palestra con autenticazione **JWT**.

## 🚀 Ruoli
- **USER**: cliente, vede schede e calendario, segna progressi
- **TRAINER**: crea esercizi e schede
- **SUPERVISOR**: gestisce utenti, trainer e statistiche

## ✨ Funzionalità principali
- CRUD per utenti, trainer, esercizi e schede
- Autenticazione JWT (login, registrazione, logout)
- Protezione endpoint per ruolo
- Persistenza dati con SQLite tramite SQLAlchemy
- Migrazioni con Flask-Migrate
- Struttura MVC (models, controllers, views)
- Frontend con Bootstrap per pagine HTML responsive

## 📦 Requisiti
Vedi `requirements.txt`:
- Flask
- Flask-Smorest
- Flask-JWT-Extended
- SQLAlchemy
- Flask-Migrate
- ecc.

## 🏗️ Setup
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
