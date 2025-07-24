
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from db import db
from models.supervisor import Supervisor
from models.user import UserModel
from models.trainer import TrainerModel
from models.scheda import SchedaModel
from models.esercizio import EsercizioModel
from schemas import SupervisorSchema, UserSchema, TrainerSchema, SchedaSchema, EsercizioSchema
from utils.decorators import role_required
from controllers.supervisor_controller import SupervisorController

blp = Blueprint("supervisors", __name__, description="Operazioni sui supervisor")
supervisor_controller = SupervisorController()

@blp.route("/supervisors/<int:supervisor_id>")
class SupervisorResource(MethodView):
    @role_required('supervisor')
    @blp.response(200, SupervisorSchema)
    def get(self, supervisor_id):
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        return supervisor

@blp.route("/supervisors/dashboard")
class SupervisorDashboard(MethodView):
    @jwt_required()
    def get(self):
        result = supervisor_controller.dashboard()
        return result

@blp.route("/supervisors/utenti-trainer")
class GestisciUtentiTrainer(MethodView):
    @jwt_required()
    def get(self):
        result = supervisor_controller.gestisci_utenti_trainer()
        return result

@blp.route("/supervisors/revisione")
class RevisioneSchedeEsercizi(MethodView):
    @jwt_required()
    def get(self):
        result = supervisor_controller.revisione_schede_esercizi()
        return result
