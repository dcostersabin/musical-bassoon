from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from flask import request


def invalid_role():
    return jsonify({"status": "Invalid Role"}), 403


def add_music_permission(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 1 or info.get("role") == 2:
            return func(*args, **kwargs)
        elif (info.get("role") == 3) and (
            info.get("id") == request.json.get("user_id", 1)
        ):
            return func(*args, **kwargs)
        else:
            return invalid_role()

    return wrapper_func


def super_admin_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 1:
            return func(*args, **kwargs)
        else:
            return invalid_role()

    return wrapper_func


def artist_manager_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 2:
            return func(*args, **kwargs)
        else:
            return invalid_role()

    return wrapper_func


def artist_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 3:
            return func(*args, **kwargs)
        else:
            return invalid_role()

    return wrapper_func


def super_admin_and_artist_manager_only(func):
    def wrapper_func(*args, **kwargs):
        info = get_jwt_identity()
        if info.get("role") == 1 or info.get("role") == 2:
            return func(*args, **kwargs)
        else:
            return invalid_role()

    return wrapper_func
