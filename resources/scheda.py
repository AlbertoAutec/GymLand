from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.scheda import SchedaModel
from schemas import SchedaSchema
from utils.decorators import role_required

blp = Blueprint("schede", __name__, description="Operazioni sulle schede")

# Esempio di route base
@blp.route("/schede/<int:scheda_id>")
class SchedaResource(MethodView):
    @role_required('user', 'trainer', 'supervisor')
    @blp.response(200, SchedaSchema)
    def get(self, scheda_id):
        scheda = SchedaModel.query.get_or_404(scheda_id)
        return scheda
