from db.models import Model
from db.models import CharField, DateTimeField, ForeignKeyField
from models.users import Users


class Musics(Model):
    def __init__(self):
        super(Musics, self).__init__(tname="musics")
        self.fields.add(
            ForeignKeyField(
                name="user_id",
                references=Users(),
            )
        )
        self.fields.add(CharField(name="title"))
        self.fields.add(CharField(name="album_name"))
        self.fields.add(CharField(name="genre", length=10))
        self.fields.add(DateTimeField(name="created_at"))
        self.fields.add(DateTimeField(name="updated_at"))
