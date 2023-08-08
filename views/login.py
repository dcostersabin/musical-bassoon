from flask import request
from models.scheme import LoginScheme
from flask.views import MethodView
from marshmallow import ValidationError
from flask import jsonify
from flask_jwt_extended import create_access_token
from services.login import LoginService


class LoginView(MethodView):
    def post(self):
        scheme = LoginScheme()
        try:
            data = scheme.load(request.json)
            login_service = LoginService(data=data)
            if not login_service.login():
                return jsonify({"email": "Invalid Email"}), 400

            access_token = create_access_token(
                identity={
                    "email": login_service.user.get("email"),
                    "role": login_service.user.get("role"),
                },
            )
            return jsonify(access_token=access_token), 200
        except ValidationError as err:
            return jsonify(err.messages), 400
