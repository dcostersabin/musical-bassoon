from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.scheme import MusicScheme
from marshmallow import ValidationError
from flask import request
from flask import jsonify
from flask import Response
from services.music_create import MusicCreateService


class MusicView(MethodView):
    @jwt_required()
    def post(self):
        scheme = MusicScheme()

        try:
            data = scheme.load(request.json)
            service = MusicCreateService(data=data)
            service.start()
            status_code = 201 if service.status else 400
            return Response(status=status_code)
        except ValidationError as err:
            return jsonify(err.messages), 400
