import uuid  #qui importiamo uuid per generare identificatori univoci
from schemas import StoreSchema , ItemSchema #qui importiamo gli schemi per la validazione dei negozi e degli articoli
from flask import request #qui importiamo request per gestire le richieste HTTP
from flask.views import MethodView #qui importiamo MethodView per creare viste basate su classi
from flask_smorest import Blueprint, abort #qui importiamo Blueprint per creare blueprint e abort per gestire gli errori HTTP
from db import db #qui importiamo il database dal file db.py
from models import StoreModel #qui importiamo i modelli per i negozi
from sqlalchemy.exc import SQLAlchemyError , IntegrityError #qui importiamo SQLAlchemyError per gestire gli errori del database

blp = Blueprint("stores", __name__, description="Operations on stores") #qui creiamo un blueprint per le operazioni sui negozi

@blp.route("/stores/<int:store_id>") #qui definiamo una route per le operazioni sui negozi
class StoreDetail(MethodView): #questa classe gestisce le operazioni sui negozi
    @blp.response(200, StoreSchema)  #qui definiamo la risposta della richiesta GET utilizzando lo schema StoreSchema
    def get(self, store_id): #questa funzione gestisce le richieste GET per ottenere i dettagli di un negozio
        store = StoreModel.query.get_or_404(store_id)  #qui cerchiamo il negozio nel database, restituendo un errore 404 se non trovato
        return store  #qui restituiamo il negozio trovato   
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  #qui cerchiamo il negozio nel database, restituendo un errore 404 se non trovato
        db.session.delete(store)  #qui eliminiamo il negozio dalla sessione del database
        db.session.commit()  #qui salviamo le modifiche nel database
        return {"message": "Store deleted"}, 204  #qui restituiamo un messaggio di conferma e lo stato HTTP 204 (No Content)

@blp.route("/stores")  #qui definiamo una route per ottenere tutti i negozi
class StoreList(MethodView):  #questa classe gestisce le operazioni sui negozi
    @blp.response(200, StoreSchema(many=True))  #qui definiamo la risposta della richiesta GET utilizzando lo schema StoreSchema con many=True per indicare che restituiamo una lista di negozi
    def get(self):  #questa funzione gestisce le richieste GET per ottenere la lista dei negozi
        return StoreModel.query.all()  #qui otteniamo tutti i negozi dal database e li restituiamo
    
    
    @blp.arguments(StoreSchema)  #qui definiamo gli argomenti della richiesta utilizzando lo schema StoreSchema
    @blp.response(201, StoreSchema)  #qui definiamo la risposta della richiesta POST utilizzando lo schema StoreSchema
    def post(self, store_data):  #questa funzione gestisce le richieste POST per creare un nuovo negozio
        store = StoreModel(**store_data)  #qui creiamo un nuovo oggetto StoreModel con i dati forniti nella richiesta

        try:
            db.session.add(store)  #qui aggiungiamo l'oggetto StoreModel alla sessione del database
            db.session.commit()  #qui salviamo le modifiche nel database

        except IntegrityError:
            abort(400, message="A store with that name already exists")
        #qui gestiamo gli errori di integrità e restituiamo un errore 400 (Bad Request)
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store")  #qui gestiamo gli errori del database e restituiamo un errore 500 (Internal Server Error)
        return store, 201  #qui restituiamo il nuovo negozio e lo stato HTTP 201 (Created)
