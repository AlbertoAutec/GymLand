from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.supervisor import Supervisor
from schemas import SupervisorSchema
from utils.decorators import role_required

blp = Blueprint("supervisors", __name__, description="Operazioni sui supervisor")

@blp.route("/supervisors/<int:supervisor_id>")
class SupervisorResource(MethodView):
    @role_required('supervisor')
    @blp.response(200, SupervisorSchema)
    def get(self, supervisor_id):
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        return supervisor
