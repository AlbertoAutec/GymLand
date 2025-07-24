import os  #qui importiamo il modulo os per gestire le variabili d'ambiente
from flask import Flask, jsonify #qui importiamo Flask per creare l'applicazione web
from flask_smorest import Api #qui importiamo Api per gestire le API RESTful
from db import db #qui importiamo il modulo db per gestire il database
import models #qui importiamo il modulo models per definire i modelli del database
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity  #qui importiamo JWTManager per gestire l'autenticazione JWT
from resources.user import blp as UsersBlueprint
from resources.trainer import blp as TrainerBlueprint
from resources.supervisor import blp as SupervisorBlueprint
from resources.scheda import blp as SchedaBlueprint
from resources.esercizio import blp as EsercizioBlueprint
from blocklist import BLOCKLIST #qui importiamo il modello Blocklist per gestire i token bloccati
from flask_migrate import Migrate  #qui importiamo Migrate per gestire le migrazioni del database



def create_app(db_url=None):
    app = Flask(__name__)
    from flask import render_template

    @app.route("/")
    def home():
        return render_template("index.html")

    # Rotte HTML
    @app.route("/dashboard")
    @jwt_required()
    def dashboard():
        user_id = get_jwt_identity()
        user = models.user.UserModel.query.filter_by(id=user_id).first()
        abbonamenti = []
        if user:
            abbonamenti = [{
                'tipo': 'Mensile',
                'scadenza': user.abbonamento_fine.strftime('%d/%m/%Y') if user.abbonamento_fine else 'N/A'
            }] if user.abbonamento_attivo() else []
        # Recupero scheda attiva
        scheda = user.schede.filter_by().first() if user else None
        pagamenti = [] # Da implementare: query pagamenti utente
        return render_template(
            "dashboard.html",
            user=user,
            abbonamenti=abbonamenti,
            scheda=scheda,
            pagamenti=pagamenti
        )

    @app.route("/scheda")
    def scheda():
        return render_template("scheda.html")

    @app.route("/esercizi")
    def esercizi():
        return render_template("esercizi.html")

    @app.route("/utenti")
    def utenti():
        return render_template("utenti.html")

    @app.route("/trainer")
    def trainer():
        return render_template("trainer.html")

    @app.route("/supervisor")
    def supervisor():
        return render_template("supervisor.html")

    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "NalaBond"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"role": "admin"}
        return {"role": "user"}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Missing authorization header", "error": "authorization_required"}), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has been revoked", "error": "token_revoked"}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Fresh token required", "error": "fresh_token_required"}), 401

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(TrainerBlueprint)
    api.register_blueprint(SupervisorBlueprint)
    api.register_blueprint(SchedaBlueprint)
    api.register_blueprint(EsercizioBlueprint)

    return app
