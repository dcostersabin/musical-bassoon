from flask.views import MethodView
from permissions import artist_manager_only
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from services.music_upload import MusicUploadService
from flask import request
from flask import jsonify
from models.scheme import MusicUploadScheme
from flask import Response


class UploadMusicView(MethodView):
    @jwt_required()
    @artist_manager_only
    def post(self):
        scheme = MusicUploadScheme()
        try:
            data = scheme.load(request.json)
            service = MusicUploadService(data=data)
            service.start()
            status_code = 201 if service.status else 400
            return Response(status=status_code)

        except ValidationError as err:
            return jsonify(err.messages), 400
