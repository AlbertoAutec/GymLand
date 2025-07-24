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
