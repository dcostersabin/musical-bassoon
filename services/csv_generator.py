import csv
from flask import Response
from models.users import Users
from models.musics import Musics
from db.crud import CRUDBase
from tempfile import TemporaryFile


class CsvGeneratorService:
    def __init__(self, artist_id: str, page_numnber=1):
        self.artist_id = artist_id
        self.file = TemporaryFile(mode="w+")
        self.page_number = page_numnber
        self.user_crud_base = CRUDBase(model=Users)
        self.music_crud_base = CRUDBase(model=Musics)
        self.user = {}
        self.musics = []
        self.status = False
        self.response = None

    def start(self):
        self._run()

    def _run(self):
        if self._check_artist():
            self._get_musics()
            self._generate_csv()
            self._generate_response()
            self.status = True

    def _check_artist(self) -> bool:
        useless_fields = ["password", "id", "role", "created_at", "updated_at"]
        data = self.user_crud_base.filter({"id": self.artist_id, "role": 3})

        if len(data) != 1:
            return False

        self.user = data[0]
        _ = [self.user.pop(field) for field in useless_fields]
        self.user["dob"] = self.user.get("dob").strftime("%Y-%m-%d %H:%M:%S")
        return True

    def _get_musics(self):
        useless_fields = ["id", "user_id", "created_at", "updated_at"]
        data = self.music_crud_base.filter(
            {"user_id": self.artist_id},
            page_number=int(self.page_number),
        )
        _ = [i.pop(field) for i in data for field in useless_fields]

        self.musics += data

    def _generate_csv(self):
        writer = csv.writer(self.file)
        headers = list(self.user.keys())
        if len(self.musics) > 0:
            headers += list(self.musics[0].keys())
        rows = []
        user_values = list(self.user.values())
        for music in self.musics:
            data = user_values + list(music.values())
            rows.append(data)

        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        self.file.seek(0)

    def _generate_response(self):
        self.response = Response(self.file, mimetype="text/csv")
        self.response.headers.set(
            "Content-Disposition",
            "attachment",
            filename=f"{self.user.get('email','Artist')}.csv",
        )
