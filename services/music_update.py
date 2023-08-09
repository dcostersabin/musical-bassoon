from datetime import datetime
from models.musics import Musics
from db.crud import CRUDBase


class MusicUpdateService:
    def __init__(self, music_id: dict, data: dict, permission: dict):
        self.data = data
        self.music_id = music_id
        self.permission = permission
        self.music_crud_base = CRUDBase(model=Musics)
        self.status = False

    def start(self) -> None:
        self._run()

    def _prep_data(self) -> None:
        self.data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _run(self) -> None:
        self._prep_data()
        self._run_update_pipeline()

    def _run_update_pipeline(self) -> None:
        role = int(self.permission.get("role", 0))

        if role == 1 or role == 2:
            self._update()
            return

        if role == 3 and self._verify_user():
            self._update()
            return

    def _verify_user(self) -> bool:
        owner = self.permission.get("id", 0)
        music = self.music_crud_base.filter(
            {
                "id": self.music_id,
                "user_id": owner,
            }
        )
        return True if len(music) == 1 else False

    def _update(self) -> None:
        self.music_crud_base.update(id=self.music_id, data=self.data)
        self.status = True if len(self.music_crud_base.errors) == 0 else False
