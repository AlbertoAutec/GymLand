import os  #qui importiamo il modulo os per gestire le variabili d'ambiente
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash #qui importiamo Flask per creare l'applicazione web
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
from models.user import UserModel



def create_app(db_url=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "super-gymland-secret-key-2025"

    @app.route("/", methods=["GET"])
    def root():
        return render_template("auth.html")

    @app.route("/home", methods=["GET"])
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
    @jwt_required()
    def trainer():
        print("COOKIES (request):", dict(request.cookies))  # DEBUG
        from flask_jwt_extended import get_jwt
        jwt_token = get_jwt()
        print("JWT PAYLOAD:", jwt_token)  # DEBUG
        user_id = get_jwt_identity()
        user = models.user.UserModel.query.filter_by(id=user_id).first()
        trainer_name = user.nome if user else "Trainer"
        return render_template("trainer.html", trainer_name=trainer_name)

    @app.route("/supervisor")
    @jwt_required()
    def supervisor():
        user_id = get_jwt_identity()
        user = models.user.UserModel.query.filter_by(id=user_id).first()
        supervisor_name = user.nome if user else "Supervisor"
        return render_template("supervisor.html", supervisor_name=supervisor_name)

    @app.route("/auth", methods=["GET"])
    def auth():
        return render_template("auth.html")

    @app.route("/jwt-login", methods=["GET", "POST"])
    def jwt_login():
        if request.method == "POST":
            jwt_token = request.form.get("jwt_token")
            if not jwt_token:
                flash("Token JWT mancante.", "danger")
                return redirect(url_for("jwt_login"))
            from flask_jwt_extended import decode_token
            try:
                decoded = decode_token(jwt_token)
                user_id = decoded.get("sub")
                user = models.user.UserModel.query.filter_by(id=user_id).first()
                trainer_name = user.nome if user else "Trainer"
                return render_template("trainer.html", trainer_name=trainer_name, jwt_token=jwt_token)
            except Exception as e:
                flash(f"Token JWT non valido: {e}", "danger")
                return redirect(url_for("jwt_login"))
        # GET: mostra form per incollare il token
        return '''<html><head><meta charset="utf-8"><title>JWT Login</title></head><body>
        <h3>Accedi come trainer con JWT</h3>
        <form method="POST">
            <label for="jwt_token">Incolla qui il tuo token JWT:</label><br>
            <textarea name="jwt_token" id="jwt_token" style="width:100%;height:100px"></textarea><br>
            <button type="submit">Accedi</button>
        </form>
        </body></html>'''

    @app.route("/login", methods=["POST"])
    def login():
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        from werkzeug.security import check_password_hash
        # Login con ruolo scelto dall'utente
        user = models.user.UserModel.query.filter_by(email=email, ruolo=role).first()
        if user and check_password_hash(user.password, password):
            from flask_jwt_extended import create_access_token
            access_token = create_access_token(identity=user.id)
            print("JWT:", access_token)  # DEBUG
            # Mostra il token JWT all'utente per copia/incolla
            html = f'''<html><head><meta charset="utf-8"><title>Token JWT</title>
            <script>
                setTimeout(function() {{ window.location.href = '/home'; }}, 3000);
            </script>
            </head><body>
            <h3>Login effettuato come {role}!</h3>
            <p>Copia questo token JWT e usalo per accedere alle pagine protette:</p>
            <textarea style="width:100%;height:100px">{access_token}</textarea>
            <form method="POST" action="/token-login">
                <input type="hidden" name="jwt_token" value="{access_token}">
                <button type="submit">Accedi come {role} con questo token</button>
            </form>
            <br>
            <form action="/home" method="get">
                <button type="submit">Vai alla Home</button>
            </form>
            <p style="color:gray;font-size:small;">Verrai reindirizzato automaticamente alla home tra 3 secondi...</p>
            </body></html>'''
            from flask import make_response
            resp = make_response(html)
            return resp
        else:
            flash("Credenziali non valide o ruolo errato.", "danger")
            return redirect(url_for("root"))
    @app.route("/token-login", methods=["POST"])
    def token_login():
        jwt_token = request.form.get("jwt_token")
        # Simula la validazione del token e imposta l'identità nella sessione
        # In realtà, per usare il token senza cookie, dovresti passarlo come Authorization: Bearer ...
        # Qui mostriamo solo la pagina trainer se il token è presente
        if not jwt_token:
            flash("Token JWT mancante.", "danger")
            return redirect(url_for("root"))
        # Decodifica il token per ottenere l'user_id
        from flask_jwt_extended import decode_token
        try:
            decoded = decode_token(jwt_token)
            user_id = decoded.get("sub")
            user = models.user.UserModel.query.filter_by(id=user_id).first()
            trainer_name = user.nome if user else "Trainer"
            return render_template("trainer.html", trainer_name=trainer_name, jwt_token=jwt_token)
        except Exception as e:
            flash(f"Token JWT non valido: {e}", "danger")
            return redirect(url_for("root"))

    @app.route("/register", methods=["POST"])
    def register():
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        # Controllo se l'email esiste già
        if models.user.UserModel.query.filter_by(email=email).first():
            flash("Email già registrata!", "danger")
            return redirect(url_for("root"))
        # Hash della password
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(password)
        # Crea nuovo utente
        new_user = models.user.UserModel(
            email=email,
            password=hashed_password,
            ruolo=role,
            nome="",  # Da completare in una fase successiva
            cognome=""
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registrazione avvenuta con successo! Ora puoi accedere.", "success")
        return redirect(url_for("root"))

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
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # True solo in produzione HTTPS
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Attiva True in produzione
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_ALGORITHM"] = "HS256"
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        from flask import request
        print("[DEBUG 401] COOKIES (request):", dict(request.cookies))
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
