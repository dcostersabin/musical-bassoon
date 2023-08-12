from flask.views import MethodView
from flask_jwt_extended import jwt_required
from models.scheme import MusicScheme
from marshmallow import ValidationError
from flask import request
from flask import jsonify
from flask import Response
from models.scheme import MusicUpdateScheme
from services.music_create import MusicCreateService
from services.music_delete import MusicDeleteService
from services.music_update import MusicUpdateService
from permissions import add_music_permission
from permissions import artist_only
from flask_jwt_extended import get_jwt_identity
from models.musics import Musics
from db.crud import CRUDBase


class MusicView(MethodView):
    def __init__(self):
        self.music_crud_base = CRUDBase(model=Musics)

    def _list_users_music(self):
        info = get_jwt_identity()
        page = request.args.get("page", 1)
        data = self.music_crud_base.filter(
            {"user_id": info.get("id")},
            order_by="updated_at",
            dec=True,
            page_number=int(page),
        )
        return (
            jsonify(
                {"count": len(data), "page": int(page), "music": data},
            ),
            200,
        )

    def _list_user_music_admin_manager(self):
        page = request.args.get("page", 1)
        user_id = request.args.get("user_id", None)
        if user_id is None:
            return Response(status=400)

        data = self.music_crud_base.filter(
            {"user_id": user_id},
            order_by="title",
            dec=False,
            page_number=int(page),
        )

        return (
            jsonify(
                {"count": len(data), "page": int(page), "music": data},
            ),
            200,
        )

    @jwt_required()
    @add_music_permission
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

    @jwt_required()
    def get(self):
        info = get_jwt_identity()

        role = info.get("role")

        if role == 1 or role == 2:
            return self._list_user_music_admin_manager()

        return self._list_users_music()

    @jwt_required()
    @artist_only
    def delete(self):
        info = get_jwt_identity()
        music_id = request.args.get("music_id", None)
        if music_id is None:
            return Response(status=400)

        service = MusicDeleteService(music_id=music_id, permission=info)
        service.start()
        status_code = 204 if service.status else 400
        return Response(status=status_code)

    @jwt_required()
    @artist_only
    def put(self):
        scheme = MusicUpdateScheme()

        info = get_jwt_identity()
        music_id = request.args.get("music_id", None)
        if music_id is None:
            return Response(status=400)

        try:
            data = scheme.load(request.json)
            service = MusicUpdateService(
                music_id=music_id,
                data=data,
                permission=info,
            )
            service.start()
            status_code = 200 if service.status else 400
            return Response(status=status_code)
        except ValidationError as err:
            return jsonify(err.messages), 400
