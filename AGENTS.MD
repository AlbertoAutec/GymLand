# AGENTS – Ruoli e Permessi

## 👤 USER (Cliente Palestra)
- Può registrarsi e autenticarsi (JWT)
- Vede la propria **scheda allenamento** attiva
- Ogni giorno può segnare cosa ha completato
- Vede i suoi esercizi sul **calendario personale**
- Dati gestiti:
  - Nome, cognome, email, indirizzo
  - Abbonamento attivo (data inizio/fine)

---

## 🏋️ TRAINER
- Può autenticarsi (JWT)
- Gestisce **anagrafica esercizi** con immagini e descrizione
- Crea **schede allenamento** per gli utenti
- Ogni scheda ha:
  - Lista esercizi
  - Periodo di validità / prova
- Può generare **schede fittizie** (bozze o template)

---

## 🛡️ SUPERVISOR
- Può autenticarsi (JWT)
- Gestisce utenti e trainer (CRUD completo)
- Può visionare e modificare qualunque scheda
- Dashboard di riepilogo:
  - Utenti totali, abbonamenti attivi
  - Schede create per trainer
  - Log di attività



Sommario
Cap 1 - Di che cosa si parla.................................................................................................................1
Cap 2 - Primi passi..............................................................................................................................1
Cap 3 – Miglioramenti e Gestione degli errori ...................................................................................2
Cap 1 - Di che cosa si parla 
• API -> interfaccia per comunicare tra programmi
• REST -> un modo ordinato e standard per usare HTTP
• API REST -> un servizio web accessibile via URL e metodi http, che restituisce dati (es JSON)
STRUMENTI UTILIZZATI
• Python come linguaggio di programmazione
• Flask + estensioni :
o Flask-JWT-Extended (gestione JWT)
o Flask-SQLAlchemy (ORM)
Cap 2 - Primi passi 
I passaggi chiave sono:
1. Configurazione iniziale dell’ambiente Flask
a. Creazione e attivazione di un ambiente virtuale
b. Installazione di Flask (pip install flask)
c. Creazione del file dell’installazione ( creare un file app.py e inizializzare l’applicazione al suo 
interno)
2. Definizione della struttura dati
a. Per semplicità il primo test viene effettuato su dei dati presi da una lista di dizionari in 
Python, poi nei prossimi useremo DB
3. Creazione degli Endpoint API
a. Sono definiti usando i decoratori di Flask che associano una URL e un metodo http (GET o 
POST) a una funzione in Python
b. Tutti i metodi sono definiti in Python da @app.get o @app.post; il codice inoltra 
request.get_json() per recuperare dati JSON inviati dal client (include ad es nome negozio)
4. Esecuzione e interazione con l’API REST
a. Esecuzione dell app.py (comando flask run)
b. Usato Insomnia Rest Client per fare test manuali
c. Dopo aver avviato l’app Flask, si può inviare una richiesta da Insomnia e visuallizare la 
risposta JSON dall’API
5. Containerizzazione con Docker
a. Un’immagine Docker è un insieme di codice sorgente, librerie, dipendenze e strumenti 
necessari a un container per funzionare
b. Un container Docker è un’istanza in esecuzione di un’immagine Docker, questi ultimi sono 
+ leggeri delle VM poiché utilizzano kernel del sistema operativo host
c. Creazione di un Docker File
d. Costruzione dell’immagine Docker
e. Esecuzione del container Docker
f. Docker Compose (per semplificare l’avvio e la gestione di + container (es API e DB)
Cap 3 – Miglioramenti e Gestione degli errori 
1. Spostamento dei dati in un file separato
2. Utilizzo di ID univoci (UUID)
3. Importazione dei dati
Si passa poi alla creazione di EndPoint API con Flask-Smorest, BluePrints e MethodViews
1. Organizzazione del codice con BluePrints
2. Definizione Endpoints
3. Gestione degli errori migliorata
Validazione e Serializzazione dei Dati con Marshmallow e Flask-Smores
