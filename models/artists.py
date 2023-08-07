from db.models import Model
from db.models import CharField, DateTimeField, IntField


class Artists(Model):
    def __init__(self):
        super(Artists, self).__init__(tname="artists")
        self.fields.add(CharField(name="name"))
        self.fields.add(DateTimeField(name="dob"))
        self.fields.add(CharField(name="gender", length=1))
        self.fields.add(CharField(name="address"))
        self.fields.add(IntField(name="first_release_year"))
        self.fields.add(IntField(name="no_of_albums_released"))
        self.fields.add(DateTimeField(name="create_at"))
        self.fields.add(DateTimeField(name="updated_at"))
