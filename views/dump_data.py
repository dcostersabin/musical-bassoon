from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from permissions import artist_manager_only
from flask import Response
from services.csv_generator import CsvGeneratorService


class DumpDataView(MethodView):
    @jwt_required()
    @artist_manager_only
    def get(self):
        artist_id = request.args.get("artist_id", None)
        page = request.args.get("page", 1)
        if artist_id is None:
            return Response(status=400)

        service = CsvGeneratorService(
            artist_id=artist_id,
            page_numnber=int(page),
        )
        service.start()
        status_code = 201 if service.status else 400
        if status_code == 201:
            return service.response
        return Response(status=status_code)
