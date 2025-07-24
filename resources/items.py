from schemas import ItemSchema, ItemUpdateSchema  #qui importiamo gli schemi per la validazione degli articoli
from flask.views import MethodView #qui importiamo MethodView per creare viste basate su classi
from flask_smorest import Blueprint, abort #qui importiamo Blueprint per creare blueprint e abort per gestire gli errori HTTP
from db import db #qui importiamo il database dal file db.py
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  #qui importiamo SQLAlchemyError per gestire gli errori del database
from models import ItemModel  #qui importiamo i modelli per gli articoli
from flask_jwt_extended import jwt_required, get_jwt #qui importiamo jwt_required per proteggere le rotte con JWT


blp = Blueprint("items", __name__, description="Operations on items") #qui creiamo un blueprint per le operazioni sugli articoli

@blp.route("/items/<int:item_id>") #qui definiamo una route per le operazioni sugli articoli
class Item(MethodView): #questa classe gestisce le operazioni sugli articoli
    @jwt_required()  #qui proteggiamo la rotta con JWT, richiedendo un token valido per accedere
    @blp.response(200, ItemSchema)  #qui definiamo la risposta della richiesta GET utilizzando lo schema ItemSchema
    def get(self, item_id): #questa funzione gestisce le richieste GET per ottenere i dettagli di un articolo
       item = ItemModel.query.get_or_404(item_id)  #qui cerchiamo l'articolo nel database, restituendo un errore 404 se non trovato
       return item  #qui restituiamo l'articolo trovato
    
    @jwt_required()  #qui proteggiamo la rotta con JWT, richiedendo un token valido per accedere
    def delete(self, item_id):
       jwt = get_jwt()  #qui otteniamo il token JWT dalla richiesta
       if jwt["role"] != "admin":  #qui verifichiamo se l'utente ha il ruolo di admin
           abort(403, message="You do not have permission to delete this item")
       #qui gestiamo gli errori di autorizzazione e restituiamo un errore 403 (Forbidden)
       item = ItemModel.query.get_or_404(item_id)  #qui cerchiamo l'articolo nel database, restituendo un errore 404 se non trovato
       db.session.delete(item)  #qui eliminiamo l'articolo dalla sessione del database
       db.session.commit()  #qui salviamo le modifiche nel database
       return {"message": "Item deleted"}, 204  #qui restituiamo un messaggio di conferma e lo stato HTTP 204 (No Content)

    @blp.arguments(ItemUpdateSchema)  #qui definiamo gli argomenti della richiesta utilizzando lo schema ItemUpdateSchema
    @blp.response(200, ItemSchema)  #qui definiamo la risposta della richiesta PUT utilizzando lo schema ItemSchema
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)  #qui cerchiamo l'articolo nel database
        if item:
            if "name" in item_data:
                item.name = item_data["name"]
            if "price" in item_data:
                item.price = item_data["price"]
            if "store_id" in item_data:
                item.store_id = item_data["store_id"]
        else:
            item = ItemModel(id=item_id, **item_data)  #qui creiamo un nuovo oggetto ItemModel con i dati forniti nella richiesta   
        db.session.add(item)  #qui aggiungiamo l'oggetto ItemModel alla sessione del database
        db.session.commit()  #qui salviamo le modifiche nel database
        return item  #qui restituiamo l'articolo aggiornato
    
@blp.route("/items")  #qui definiamo una route per ottenere tutti gli articoli
class ItemList(MethodView):  #questa classe gestisce le operazioni sugli articoli
    @jwt_required()  #qui proteggiamo la rotta con JWT, richiedendo un token valido per accedere
    @blp.response(200, ItemSchema(many=True))  #qui definiamo la risposta della richiesta GET utilizzando lo schema ItemSchema con many=True per indicare che restituiamo una lista di articoli
    def get(self):  #questa funzione gestisce le richieste GET per ottenere la lista degli articoli
        items = ItemModel.query.all()  #qui otteniamo tutti gli articoli dal database
        return items  #qui restituiamo la lista degli articoli

    @jwt_required(fresh=True)  #qui proteggiamo la rotta con JWT, richiedendo un token valido per accedere
    @blp.arguments(ItemSchema)  #qui definiamo gli argomenti della richiesta utilizzando lo schema ItemSchema
    @blp.response(201, ItemSchema)  #qui definiamo la risposta della richiesta POST utilizzando lo schema ItemSchema
    def post(self, item_data):  #questa funzione gestisce le richieste POST per creare un nuovo articolo
        item = ItemModel(**item_data)  #qui creiamo un nuovo oggetto ItemModel con i dati forniti nella richiesta

        try:
            db.session.add(item)  #qui aggiungiamo l'oggetto ItemModel alla sessione del database
            db.session.commit()  #qui salviamo le modifiche nel database
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the item")  #qui gestiamo gli errori del database e restituiamo un errore 500 (Internal Server Error)
        return item, 201  #qui restituiamo il nuovo articolo e lo stato HTTP 201 (Created)


