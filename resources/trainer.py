from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.trainer import TrainerModel
from schemas import TrainerSchema
from utils.decorators import role_required

blp = Blueprint("trainers", __name__, description="Operazioni sui trainer")

@blp.route("/trainers/<int:trainer_id>")
class TrainerResource(MethodView):
    @role_required('trainer', 'supervisor')
    @blp.response(200, TrainerSchema)
    def get(self, trainer_id):
        trainer = TrainerModel.query.get_or_404(trainer_id)
        return trainer
