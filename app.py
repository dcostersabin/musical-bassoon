from flask import Flask
from config import get_config
from models.users import Users
from models.artists import Artists
from models.musics import Musics
from models.roles import Roles
from models.user_roles import UserRoles
from ordered_set import OrderedSet
from db.models.check import CheckTables

app = Flask(__name__)
config = get_config()
app.config.from_object(config)

models = OrderedSet([Roles, Users, Artists, Musics, UserRoles])

CheckTables(models=models).start()
