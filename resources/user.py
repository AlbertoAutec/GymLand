from flask.views import MethodView  #qui importiamo MethodView per creare viste basate su classi    
from flask_smorest import Blueprint, abort  #qui importiamo Blueprint per creare blueprint e abort per gestire gli errori HTTP
from db import db  #qui importiamo il database dal file db.py
from models import UserModel  #qui importiamo il modello degli utenti
from schemas import UserSchema  #qui importiamo lo schema per la validazione degli utenti
from flask_jwt_extended import (
    create_access_token , #qui importiamo create_access_token per gestire l'autenticazione JWT
    create_refresh_token,  #qui importiamo create_refresh_token per gestire i refresh token
    get_jwt_identity,  #qui importiamo get_jwt_identity per ottenere l'identità dell'utente dal token JWT
    get_jwt, #qui importiamo get_jwt per ottenere il token JWT dalla richiesta
    jwt_required,  #qui importiamo jwt_required per proteggere le rotte con JWT
)

from passlib.hash import pbkdf2_sha256  #qui importiamo pbkdf2_sha256 per gestire l'hashing delle password
from blocklist import BLOCKLIST  #qui importiamo il modello Blocklist per gestire i token bloccati

blp = Blueprint("Users", "users", description="Operations on users")  #qui creiamo un blueprint per le operazioni sugli utenti

@blp.route("/register")  #qui definiamo la route per la registrazione degli utenti
class UserRegister(MethodView):  #questa classe gestisce le operazioni di registrazione degli utenti
    @blp.arguments(UserSchema)  #qui definiamo gli argomenti della richiesta utilizzando lo schema UserSchema
    @blp.response(201, UserSchema)  # aggiungi questa riga per serializzare correttamente la risposta
    def post(self, user_data):  #questa funzione gestisce le richieste POST per registrare un nuovo utente
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():  #qui verifichiamo se esiste già un utente con lo stesso username
            abort(400, message="Username already exists")  #qui gestiamo gli errori di integrità e restituiamo un errore 400

        user = UserModel(
            username=user_data["username"],  #qui creiamo un nuovo oggetto UserModel con lo username fornito nella richiesta
            password=pbkdf2_sha256.hash(user_data["password"])  #qui hashiamo la password dell'utente prima di salvarla nel database            
        )
        db.session.add(user)  #qui aggiungiamo il nuovo utente alla sessione del database
        db.session.commit()  #qui confermiamo le modifiche al database
        return user, 201  #qui restituiamo l'utente creato e un codice di stato 201
    
@blp.route("/user/<int:user_id>")  #qui definiamo la route per ottenere i dettagli di un utente specifico
class UserDetail(MethodView):  #questa classe gestisce le operazioni sugli utenti
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)  #qui eliminiamo l'utente dalla sessione del database
        db.session.commit()  #qui salviamo le modifiche nel database
        return {"message": "User deleted"}, 204  #qui restituiamo un messaggio di conferma e lo stato HTTP 204 (No Content)

@blp.route("/login")  #qui definiamo la route per il login degli utenti
class UserLogin(MethodView):  #questa classe gestisce le operazioni di login degli utenti
    @blp.arguments(UserSchema)  #qui definiamo gli argomenti della richiesta
    def post(self, user_data): #qui gestiamo le richieste POST per il login degli utenti
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first() #qui cerchiamo l'utente nel database

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)  #qui creiamo un token di accesso JWT per l'utente autenticato
            refresh_token = create_refresh_token(str(user.id))  #qui creiamo un token di refresh JWT per l'utente autenticato (identity coerente)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials")  #qui gestiamo gli errori di autenticazione e restituiamo un errore 401 (Unauthorized)

@blp.route("/logout")  #qui definiamo la route per il logout degli utenti
class UserLogout(MethodView):  #questa classe gestisce le operazioni di logout degli utenti
    @jwt_required()  #qui proteggiamo la rotta con JWT, richiedendo un token valido per accedere
    def post(self):  #questa funzione gestisce le richieste POST per il logout degli utenti
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out successfully"}, 200  #qui restituiamo un messaggio di successo e lo stato HTTP 200 (OK)
    
@blp.route("/refresh")  #qui definiamo la route per il refresh del token JWT
class TokenRefresh(MethodView):  #questa classe gestisce le operazioni di refresh del token
    @jwt_required(refresh=True)  #qui proteggiamo la rotta con JWT, richiedendo un token di refresh valido per accedere
    def post(self):  #questa funzione gestisce le richieste POST per il refresh del token
        current_user = get_jwt_identity()  #qui otteniamo l'identità dell'utente dal token JWT
        new_token = create_access_token(identity=current_user, fresh=False)  #qui creiamo un nuovo token di accesso JWT per l'utente corrente
        jti = get_jwt()["jti"]  #qui otteniamo l'identificatore del token (jti) dal token JWT
        BLOCKLIST.add(jti)  #qui aggiungiamo il jti alla lista dei token bloccati
        return {"access_token": new_token}, 200  #qui restituiamo il nuovo token di accesso e lo stato HTTP 200 (OK)

@blp.route("/user")  #qui definiamo la route per ottenere tutti gli utenti
class UserList(MethodView):  #questa classe gestisce la lista degli utenti
    @blp.response(200, UserSchema(many=True))  #qui definiamo la risposta della richiesta GET utilizzando lo schema UserSchema con many=True
    def get(self):  #questa funzione gestisce le richieste GET per ottenere la lista degli utenti
        users = UserModel.query.all()  #qui otteniamo tutti gli utenti dal database
        return users  #qui restituiamo la lista degli utenti

