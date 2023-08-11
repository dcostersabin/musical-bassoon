from flask.views import MethodView
from flask import request
from models.scheme import UserScheme
from flask import jsonify
from marshmallow import ValidationError
from services.user_create import UserCreateService


class RegisterUserView(MethodView):
    def post(self):
        scheme = UserScheme()

        try:
            data = scheme.load(request.json)
            service = UserCreateService(data=data)
            service.start()
            status_code = 201 if service.status else 400
            return jsonify({"id": service.id}), status_code

        except ValidationError as err:
            return jsonify(err.messages), 400
