from models.musics import Musics
from db.crud import CRUDBase


class MusicDeleteService:
    def __init__(self, music_id: str, permission: dict):
        self.music_id = music_id
        self.permission = permission
        self.music_crud_base = CRUDBase(model=Musics)
        self.status = False

    def start(self):
        self._run()

    def _run(self):
        self._run_delete_pipeline()

    def _run_delete_pipeline(self):
        role = int(self.permission.get("role", 0))

        if role == 1 or role == 2:
            self._delete()
            return

        if role == 3 and self._verify_user():
            self._delete()
            return

    def _delete(self):
        self.music_crud_base.delete(id=self.music_id)
        self.status = True if len(self.music_crud_base.errors) == 0 else False

    def _verify_user(self) -> bool:
        owner = self.permission.get("id", 0)
        music = self.music_crud_base.filter({"id": self.music_id, "user_id": owner})
        return True if len(music) == 1 else False
