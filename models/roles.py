from db.models import Model
from db.models import CharField


class Roles(Model):
    def __init__(self):
        super(Roles, self).__init__(tname="roles")
        self.fields.add(CharField(name="role_name", unique=True))
