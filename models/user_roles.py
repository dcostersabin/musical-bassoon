from db.models import Model
from models.roles import Roles
from models.users import Users
from db.models import ForeignKeyField


class UserRoles(Model):
    def __init__(self):
        super(UserRoles, self).__init__(tname="user_roles")
        self.fields.add(ForeignKeyField(name="role_id", references=Roles()))
        self.fields.add(ForeignKeyField(name="user_id", references=Users()))
