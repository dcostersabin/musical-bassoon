from datetime import datetime
from models.users import Users
from models.musics import Musics
from db.crud import CRUDBase


class MusicCreateService:
    def __init__(self, data: dict):
        self.user_crud_base = CRUDBase(model=Users)
        self.music_crud_base = CRUDBase(model=Musics)
        self.data = data
        self.user = None
        self.status = False

    def start(self):
        self._run()

    def _prep_data(self):
        self.data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _run(self):
        if self.check_user():
            self._prep_data()
            self._save()

    def _save(self):
        self.music_crud_base.insert(data=self.data)
        self.status = True if len(self.music_crud_base.errors) == 0 else False

    def check_user(self) -> bool:
        data = {"id": self.data.get("user_id", 0), "role": 3}
        user = self.user_crud_base.filter(data=data)
        if len(user) == 1:
            self.user = user[0]
            return True
        else:
            return False
