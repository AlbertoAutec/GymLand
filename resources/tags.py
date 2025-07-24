#qua definiamo le risorse per i tag
from flask.views import MethodView  #qui importiamo MethodView per definire le risorse
from flask_smorest import Blueprint, abort  #qui importiamo Blueprint per creare blueprint e abort per gestire gli errori HTTP
from db import db  #qui importiamo il database
from sqlalchemy.exc import SQLAlchemyError, IntegrityError  #qui importiamo SQLAlchemyError per gestire gli errori del database
from models import TagModel, StoreModel, ItemModel  #qui importiamo il modello per i tag e i negozi
from schemas import TagSchema, TagAndItemSchema  #qui importiamo lo schema per i tag

blp = Blueprint("Tags", "tags", __name__, description="Operations on tags")  #qui creiamo un blueprint per le operazioni sui tag

@blp.route("/stores/<int:store_id>/tags")  # route corretta per i tag di uno store
class TagInStore(MethodView):  #questa classe gestisce le operazioni sui tag
    @blp.response(200, TagSchema(many=True))  #qui definiamo la risposta della richiesta GET utilizzando lo schema TagSchema
    def get(self, store_id):  #questa funzione gestisce le richieste GET per ottenere i tag di un negozio
        store = StoreModel.query.get_or_404(store_id)  #qui cerchiamo il negozio nel database, restituendo un errore 404 se non trovato
        return store.tags.all()  #qui restituiamo i tag trovati
        
    @blp.arguments(TagSchema)  #qui definiamo gli argomenti della richiesta utilizzando lo schema TagSchema
    @blp.response(201, TagSchema)  #qui definiamo la risposta della richiesta POST utilizzando lo schema TagSchema
    def post(self, tag_data, store_id):  #questa funzione gestisce le richieste POST per creare un nuovo tag
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first(): #qui verifichiamo se esiste già un tag con lo stesso nome nel negozio specificato
            abort(400, message="A tag with that name already exists in this store")  #qui gestiamo gli errori di integrità e restituiamo un errore 400
        
        tag = TagModel(**tag_data, store_id=store_id)  #qui creiamo un nuovo oggetto TagModel con i dati forniti nella richiesta e l'id del negozio
        try:
            db.session.add(tag)  #qui aggiungiamo l'oggetto TagModel alla sessione del database
            db.session.commit()  #qui salviamo le modifiche nel database
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred while creating the tag: {str(e)}")  #qui gestiamo gli errori del database e restituiamo un errore 500

        return tag, 201  #qui restituiamo il nuovo tag e lo stato HTTP 201 (Created)
    

@blp.route("/items/<int:item_id>/tags/<int:tag_id>")  #qui definiamo la route per associare o rimuovere un tag da un articolo
class LinkTagsToItem(MethodView):
    @blp.response(200, TagAndItemSchema)  #qui definiamo la risposta della richiesta POST utilizzando lo schema TagAndItemSchema
    def post(self, item_id, tag_id):  #questa funzione gestisce la richiesta POST per associare un tag a un articolo
        item = ItemModel.query.get_or_404(item_id)  #qui cerchiamo l'articolo nel database, restituendo un errore 404 se non trovato
        tag = TagModel.query.get_or_404(tag_id)  #qui cerchiamo il tag nel database, restituendo un errore 404 se non trovato
        if tag not in item.tags:  #se il tag non è già associato all'articolo
            item.tags.append(tag)  #associamo il tag all'articolo
            try:
                db.session.commit()  #salviamo le modifiche nel database
            except SQLAlchemyError as e:
                abort(500, message=f"Si è verificato un errore durante l'associazione del tag all'articolo: {str(e)}")  #gestiamo eventuali errori del database
        return {"message": "Tag associato all'articolo con successo", "tag": tag, "item": item}, 200  #restituiamo un messaggio di successo

    @blp.response(200, TagAndItemSchema)  #qui definiamo la risposta della richiesta DELETE utilizzando lo schema TagAndItemSchema
    def delete(self, item_id, tag_id):  #questa funzione gestisce la richiesta DELETE per rimuovere un tag da un articolo
        item = ItemModel.query.get_or_404(item_id)  #qui cerchiamo l'articolo nel database, restituendo un errore 404 se non trovato
        tag = TagModel.query.get_or_404(tag_id)  #qui cerchiamo il tag nel database, restituendo un errore 404 se non trovato
        if tag in item.tags:  #se il tag è associato all'articolo
            item.tags.remove(tag)  #rimuoviamo il tag dall'articolo
            try:
                db.session.commit()  #salviamo le modifiche nel database
            except SQLAlchemyError as e:
                abort(500, message=f"Si è verificato un errore durante la rimozione del tag dall'articolo: {str(e)}")  #gestiamo eventuali errori del database
            return {"message": "Tag rimosso dall'articolo con successo", "tag": tag, "item": item}, 200  #restituiamo un messaggio di successo
        abort(404, message="Tag non associato a questo articolo")  #se il tag non è associato all'articolo, restituiamo errore 404

@blp.route("/tags/<int:tag_id>")  # route corretta per il singolo tag
class Tag(MethodView):  #questa classe gestisce le operazioni sui tag specifici
    @blp.response(200, TagSchema)  #qui definiamo la risposta della richiesta GET utilizzando lo schema TagSchema
    def get(self, tag_id):  #questa funzione gestisce le richieste GET per ottenere i dettagli di un tag
        tag = TagModel.query.get_or_404(tag_id)  #qui cerchiamo il tag nel database, restituendo un errore 404 se non trovato
        return tag  #qui restituiamo il tag trovato

    @blp.response(
        202,
        description="Deletes a tag if no items are associated",  #qui definiamo la risposta della richiesta DELETE
        example={"message": "Tag deleted"},  #qui definiamo un esempio di risposta per la richiesta DELETE
    )
    @blp.alt_response(
        404, 
        description="Tag not found"
        )  #qui definiamo una risposta alternativa per il caso in cui il tag non sia trovato
    @blp.alt_response(
        400, 
        description="Tag cannot be deleted because it is associated with items"
        )  #qui definiamo una risposta alternativa per il caso in cui il tag non possa essere eliminato perché associato a degli articoli
    def delete(self, tag_id):  #questa funzione gestisce le richieste DELETE per eliminare un tag
        tag = TagModel.query.get_or_404(tag_id)  #qui cerchiamo il tag nel database, restituendo un errore 404 se non trovato

        if not tag.items:
            db.session.delete(tag)  #qui eliminiamo il tag dalla sessione del database
            db.session.commit()  #qui salviamo le modifiche nel database
            return {"message": "Tag deleted"}, 202  #qui restituiamo un messaggio di conferma e lo stato HTTP 202 (Accepted
        abort(400, message="Tag cannot be deleted because it is associated with items")  #qui gestiamo il caso in cui il tag non possa essere eliminato perché associato a degli articoli e restituiamo un errore 400 (Bad Request)

