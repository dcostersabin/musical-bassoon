from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from permissions import super_admin_only
from flask import request
from models.users import Users
from flask import Response
from db.crud import CRUDBase
from flask import jsonify
from services.user_update import UserUpdateService
from models.scheme import UserUpdateScheme
from permissions import super_admin_and_artist_manager_only


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
        data = self.crud_base.filter(data={"role": role}, page_number=int(page))
        _ = [i.pop("password") for i in data]
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

    @jwt_required()
    @super_admin_only
    def delete(self):
        user_id = request.args.get("id", None)
        if user_id is None:
            return jsonify(), 400

        self.crud_base.delete(id=user_id)

        code = 204 if len(self.crud_base.errors) == 0 else 400

        return jsonify(), code

    @jwt_required()
    @super_admin_and_artist_manager_only
    def put(self):
        user_id = request.args.get("user_id", None)
        if user_id is None:
            return Response(status=400)

        scheme = UserUpdateScheme()

        try:
            data = scheme.load(request.json)
            service = UserUpdateService(id=user_id, data=data)
            service.start()
            status_code = 202 if service.status else 400
            return Response(status=status_code)
        except ValidationError as err:
            return jsonify(err.messages), 400
