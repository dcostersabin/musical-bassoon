from datetime import datetime
from models.users import Users
from models.musics import Musics
from db.crud import CRUDBase


class MusicUploadService:
    def __init__(self, data: dict):
        self.user_crud_base = CRUDBase(model=Users)
        self.music_crud_base = CRUDBase(model=Musics)
        self.data = data
        self.user = None
        self.status = False

    def start(self):
        self._run()

    def _prep_data(self):
        self.data["user_id"] = self.user.get("id", 0)
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
        data = {"email": self.data.get("email", 0), "role": 3}
        user = self.user_crud_base.filter(data=data)
        if user is None:
            return False

        if len(user) == 1:
            self.user = user[0]
            return True
        else:
            return False
