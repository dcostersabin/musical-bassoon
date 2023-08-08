from flask_jwt_extended import get_jwt_identity
from flask import Response


def super_admin_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 1:
            func(*args, **kwargs)

        return Response({"status": "Invalid Role"}, 403)

    return wrapper_func


def artist_manager_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 2:
            func(*args, **kwargs)

        return Response({"status": "Invalid Role"}, 403)

    return wrapper_func


def artist_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 3:
            func(*args, **kwargs)

        return Response({"status": "Invalid Role"}, 403)

    return wrapper_func


def super_admin_and_artist_manager_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 1 or info.get("role") == 2:
            func(*args, **kwargs)

        return Response({"status": "Invalid Role"}, 403)

    return wrapper_func
