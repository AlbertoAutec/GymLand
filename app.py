import os  #qui importiamo il modulo os per gestire le variabili d'ambiente
from flask import Flask, jsonify #qui importiamo Flask per creare l'applicazione web
from flask_smorest import Api #qui importiamo Api per gestire le API RESTful
from db import db #qui importiamo il modulo db per gestire il database
import models #qui importiamo il modulo models per definire i modelli del database
from resources.items import blp as ItemsBlueprint #qui importiamo il blueprint per le operazioni sugli articoli
from resources.stores import blp as StoresBlueprint #qui importiamo il blueprint per le operazioni sui negozi
from resources.tags import blp as TagsBlueprint #qui importiamo il blueprint per le operazioni sui tag  
from flask_jwt_extended import JWTManager  #qui importiamo JWTManager per gestire l'autenticazione JWT
from resources.user import blp as UsersBlueprint  #qui importiamo il blueprint per le operazioni sugli utenti
from blocklist import BLOCKLIST #qui importiamo il modello Blocklist per gestire i token bloccati
from flask_migrate import Migrate  #qui importiamo Migrate per gestire le migrazioni del database


def create_app(db_url=None): #qui definiamo la funzione per creare l'applicazione Flask
    app = Flask(__name__)   #qui creiamo l'istanza dell'applicazione Flask

    app.config["API_TITLE"] = "Stores REST API"  #qui impostiamo il titolo dell'API
    app.config["API_VERSION"] = "v1"  #qui impostiamo la versione
    app.config["OPENAPI_VERSION"] = "3.0.3"  #qui impostiamo la versione di OpenAPI
    app.config["OPENAPI_URL_PREFIX"] = "/"  #qui impostiamo il prefisso URL per l'OpenAPI
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  #qui impostiamo il percorso per l'interfaccia Swagger UI
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  #qui impostiamo l'URL per caricare Swagger UI   
    app.config["PROPAGATE_EXCEPTIONS"] = True  #qui impostiamo la propagazione delle eccezioni per Flask-Smorest
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  #qui disabilitiamo il tracciamento delle modifiche di SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")  #qui impostiamo l'URI del database, utilizzando un valore predefinito se non è specificato
    db.init_app(app)  #qui inizializziamo l'applicazione Flask con il database
    migrate = Migrate(app, db)  #qui inizializziamo Migrate per gestire le migrazioni del database
    api = Api(app) #qui creiamo l'istanza dell'API RESTful

    app.config["JWT_SECRET_KEY"] = "NalaBond"  #qui impostiamo la chiave segreta per JWT, utilizzata per firmare i token 

    jwt = JWTManager(app)  #qui inizializziamo JWTManager per gestire l'autenticazione JWT

    @jwt.additional_claims_loader  #qui definiamo un gestore per aggiungere ulteriori informazioni ai token JWT
    def add_claims_to_jwt(identity):  #questa funzione aggiunge ulteriori informazioni ai token JWT
        if identity == 1:  #se l'identità è "admin"
            return {"role": "admin"}
        return {"role": "user"}


    @jwt.expired_token_loader  #qui definiamo un gestore per i token scaduti
    def expired_token_callback(jwt_header, jwt_payload):  #questa funzione gestisce i token scaduti
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401  #qui restituiamo un messaggio di errore e lo stato HTTP 401 (Unauthorized
    
    @jwt.invalid_token_loader  #qui definiamo un gestore per i token non validi
    def invalid_token_callback(error):  #questa funzione gestisce i token non validi
        return jsonify({"message": "Invalid token", "error": "invalid_token"}), 401  #qui restituiamo un messaggio di errore e lo stato HTTP 401 (Unauthorized
    
    @jwt.unauthorized_loader  #qui definiamo un gestore per le richieste non autorizzate
    def missing_token_callback(error):  #questa funzione gestisce le richieste senza token
        return jsonify({"message": "Missing authorization header", "error": "authorization_required"}), 401  #qui restituiamo un messaggio di errore e lo stato HTTP 401 (Unauthorized)
    

    @jwt.token_in_blocklist_loader  #qui definiamo un gestore per i token bloccati
    def check_if_token_in_blocklist(jwt_header, jwt_payload):  #questa funzione verifica se un token è bloccato
        return jwt_payload["jti"] in BLOCKLIST  #qui controlliamo se l'identificatore del token (jti) è presente nella lista dei token bloccati 
    
    @jwt.revoked_token_loader  #qui definiamo un gestore per i token revocati
    def revoked_token_callback(jwt_header, jwt_payload):  #questa funzione gestisce i token revocati
        return jsonify({"message": "Token has been revoked", "error": "token_revoked"}), 401  #qui restituiamo un messaggio di errore e lo stato HTTP 401 (Unauthorized)
    
    @jwt.needs_fresh_token_loader  #qui definiamo un gestore per i token che richiedono un refresh
    def needs_fresh_token_callback(jwt_header, jwt_payload):  #questa funzione gestisce i token che richiedono un refresh
        return jsonify({"message": "Fresh token required", "error": "fresh_token_required"}), 401  #qui restituiamo un messaggio di errore e lo stato HTTP 401 (Unauthorized)


    api.register_blueprint(ItemsBlueprint) #qui registriamo il blueprint per le operazioni sugli articoli
    api.register_blueprint(StoresBlueprint) #qui registriamo il blueprint per le operazioni sui negozi
    api.register_blueprint(TagsBlueprint)  #qui registriamo il blueprint per le operazioni sui tag  
    api.register_blueprint(UsersBlueprint)  #qui registriamo il blueprint per le operazioni sugli utenti

    return app  #qui restituiamo l'istanza dell'applicazione Flask
