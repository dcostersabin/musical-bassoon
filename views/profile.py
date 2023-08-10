from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from db.crud import CRUDBase
from models.users import Users
from flask import jsonify


class ProfileView(MethodView):
    def __init__(self):
        self.user_crud_base = CRUDBase(Users)

    def _get_user_info(self):
        info = get_jwt_identity()
        data = self.user_crud_base.get_one(id=info.get("id", 0))
        data.pop("password")
        return jsonify(data), 200

    @jwt_required()
    def get(self):
        return self._get_user_info()
