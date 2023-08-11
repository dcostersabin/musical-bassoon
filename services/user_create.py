from datetime import datetime
from werkzeug.security import generate_password_hash
from models.users import Users
from db.crud import CRUDBase


class UserCreateService:
    def __init__(self, data: dict):
        self.data = data
        self.status = False
        self.id = None

    def start(self):
        self._run()

    def _run(self):
        self._prep_data()
        self._save()

    def _prep_data(self):
        self.data["password"] = generate_password_hash(
            self.data.get("password"),
            method="scrypt",
        )
        self.data["dob"] = self.data.get("dob").strftime("%Y-%m-%d %H:%M:%S")
        self.data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _save(self):
        crud_obj = CRUDBase(model=Users)
        data = crud_obj.insert(data=self.data)
        if data is not None:
            self.id = data.get("id", None)
        self.status = True if len(crud_obj.errors) == 0 else False
