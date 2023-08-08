from models.roles import Roles
from db.crud import CRUDBase


class Preload:
    def start(self):
        self._run()

    def _run(self):
        self._insert_roles()

    def _insert_roles(self):
        crud_obj = CRUDBase(model=Roles)
        roles = {1: "super_admin", 2: "artist_manager", 3: "artist"}
        for role in roles:
            if crud_obj.get_one(id=role) is None:
                crud_obj.insert({"role_name": roles.get(role)})
