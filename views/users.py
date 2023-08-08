from flask.views import MethodView
from flask_jwt_extended import jwt_required
from permissions import super_admin_only
from flask import request
from models.users import Users
from db.crud import CRUDBase
from flask import jsonify


class UserView(MethodView):
    def __init__(self):
        self.crud_base = CRUDBase(model=Users)
        self.roles = {1, 2, 3}

    def _get_single_user(self):
        data = self.crud_base.get_one(id=request.args.get("id"))
        data.pop("password")
        return jsonify({"user": data}), 200

    def _get_all_users(self):
        page = request.args.get("page", 1)
        data = self.crud_base.all(page_number=int(page))
        _ = [i.pop("password") for i in data]
        return jsonify({"count": len(data), "page": int(page), "user": data}), 200

    def _get_filtered_users(self):
        page = request.args.get("page", 1)
        role = int(request.args.get("role", 1))
        data = self.crud_base.filter(data={"role": role}, page_number=page)
        return jsonify({"count": len(data), "page": int(page), "user": data}), 200

    @jwt_required()
    @super_admin_only
    def get(self):
        if request.args.get("id", None) is not None:
            return self._get_single_user()

        role = request.args.get("role", None)

        if role is not None and int(role) in self.roles:
            return self._get_filtered_users()

        return self._get_all_users()
