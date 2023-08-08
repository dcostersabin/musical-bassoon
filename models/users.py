from db.models import Model
from models.roles import Roles
from db.models import CharField, DateTimeField, ForeignKeyField


class Users(Model):
    def __init__(self):
        super(Users, self).__init__(tname="users")
        self.fields.add(CharField(name="first_name"))
        self.fields.add(CharField(name="last_name"))
        self.fields.add(CharField(name="email", unique=True))
        self.fields.add(CharField(name="password", length=500))
        self.fields.add(CharField(name="phone", length=20))
        self.fields.add(DateTimeField(name="dob"))
        self.fields.add(CharField(name="gender", length=1))
        self.fields.add(CharField(name="address"))
        self.fields.add(DateTimeField(name="created_at"))
        self.fields.add(DateTimeField(name="updated_at"))
        self.fields.add(ForeignKeyField(name="role", references=Roles()))
