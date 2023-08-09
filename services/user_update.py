from datetime import datetime
from models.users import Users
from db.crud import CRUDBase


class UserUpdateService:
    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data
        self.user_crud_base = CRUDBase(model=Users)
        self.status = False

    def start(self):
        self._run()

    def _run(self):
        self._prep_data()
        self._update()

    def _prep_data(self):
        self.data["dob"] = self.data.get("dob").strftime("%Y-%m-%d %H:%M:%S")
        self.data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _update(self):
        self.user_crud_base.update(id=self.id, data=self.data)
        self.status = True if len(self.user_crud_base.errors) == 0 else False
