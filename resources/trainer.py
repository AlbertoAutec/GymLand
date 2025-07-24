
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import db
from models.trainer import TrainerModel
from models.scheda import SchedaModel
from models.esercizio import EsercizioModel
from schemas import TrainerSchema, SchedaSchema, EsercizioSchema
from utils.decorators import role_required
from controllers.trainer_controller import TrainerController

blp = Blueprint("trainers", __name__, description="Operazioni sui trainer")
trainer_controller = TrainerController()

@blp.route("/trainers/<int:trainer_id>")
class TrainerResource(MethodView):
    @role_required('trainer', 'supervisor')
    @blp.response(200, TrainerSchema)
    def get(self, trainer_id):
        trainer = TrainerModel.query.get_or_404(trainer_id)
        return trainer

@blp.route("/trainers/<int:trainer_id>/scheda")
class CreaScheda(MethodView):
    @jwt_required()
    def post(self, trainer_id):
        # dati_scheda dovrebbe arrivare dal body della richiesta
        dati_scheda = {}
        scheda = trainer_controller.crea_scheda(trainer_id, dati_scheda)
        return SchedaSchema().dump(scheda)

@blp.route("/trainers/<int:trainer_id>/esercizio")
class CrudEsercizi(MethodView):
    @jwt_required()
    def post(self, trainer_id):
        dati_esercizio = {}
        esercizio = trainer_controller.crud_esercizi(trainer_id, dati_esercizio)
        return EsercizioSchema().dump(esercizio)
