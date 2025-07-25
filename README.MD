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






# Prompt per GitHub Copilot Pro

Voglio che tu generi un progetto Python completo.

## Obiettivo
Sviluppare una chat API (REST) che usa **Ollama** come modello di AI, integrata con:
- **Autenticazione JWT** (login utenti)
- **Database SQL Server** per salvare utenti, sessioni e messaggi
- Possibilità per ogni utente di scegliere **quale modello Ollama** utilizzare per la chat
- Tutto su ambiente **Windows**, usando **Visual Studio Code**

## Stack tecnologico
- Linguaggio: **Python 3.10+**
- Framework web: **Flask** (pattern MVC semplice)
- Database: **SQL Server** (usa `pyodbc` o `pymssql` per connetterti)
- ORM: **SQLAlchemy**
- Autenticazione: **JWT** con la libreria `PyJWT`
- Richieste verso Ollama: chiamate HTTP/locale a Ollama (presente sul mio PC)
- Frontend: per ora non serve, bastano API REST (userò Postman per testarle)

## Funzionalità da implementare
1. **Registrazione utenti** (username, email, password hashata con `werkzeug.security`)
2. **Login utenti** che genera un JWT valido per 1h
3. **Endpoint protetto** `/chat` dove:
   - l’utente autenticato sceglie il modello Ollama (`llama3`, `mistral`, ecc.)
   - invia un messaggio (`prompt`) e riceve la risposta
   - salva nel database: utente, prompt, risposta, timestamp, modello scelto
4. **Endpoint GET** `/history` per ottenere la cronologia chat dell’utente autenticato
5. Gestione errori, logging e validazioni basilari
6. Struttura progetto in cartelle tipo:


/app
/models
/routes
/services
init.py
main.py
requirements.txt


## Indicazioni aggiuntive
- Commenta il codice in modo didattico, spiegando passo passo
- Fornisci anche un esempio di file `.env` per le credenziali del DB e la secret key JWT
- Usa `pip install flask flask_sqlalchemy pyodbc PyJWT werkzeug python-dotenv requests`
- Inserisci un semplice `Dockerfile` e un `requirements.txt` di base

Genera tutto lo scheletro iniziale pronto da eseguire e spiegami con commenti cosa fa ogni file e funzione.
