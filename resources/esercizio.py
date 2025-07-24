from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.esercizio import Esercizio
from schemas import EsercizioSchema

blp = Blueprint("esercizi", __name__, description="Operazioni sugli esercizi")

@blp.route("/esercizi/<int:esercizio_id>")
class EsercizioResource(MethodView):
    @blp.response(200, EsercizioSchema)
    def get(self, esercizio_id):
        esercizio = Esercizio.query.get_or_404(esercizio_id)
        return esercizio
