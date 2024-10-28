from flask import request, Blueprint, jsonify

# from models.snack import Snack
# from models.user import User

from flask_login import login_required

router_snack = Blueprint("router_snack", __name__)


@router_snack.route("/add", methods=["POST"])
@login_required
def create_snack():
    data = request.json
    print(data)
    return jsonify({"message": "create snack"}), 200
