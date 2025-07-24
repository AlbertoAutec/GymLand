"""
blocklist.py

This file is used to manage the blocklist for JWT tokens.
It contains functions to add tokens to the blocklist and check if a token is blocked.
It will be used to prevent the reuse of tokens after logout.
Questo file è utilizzato per gestire la lista nera dei token JWT.
Contiene funzioni per aggiungere token alla lista nera e verificare se un token è bloccato.
Verrà utilizzato per prevenire il riutilizzo dei token dopo il logout.
"""
BLOCKLIST = set()  # Set to store blocked tokens