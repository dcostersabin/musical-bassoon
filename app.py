from flask import Flask
from config import get_config
from models.users import Users
from models.artists import Artists
from models.musics import Musics
from models.roles import Roles
from ordered_set import OrderedSet
from db.models.check import CheckTables
from flask_cors import CORS
from preload import Preload
from views import HealthCheckView
from views.register import RegisterUserView
from views.login import LoginView
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)

config = get_config()
app.config.from_object(config)

models = OrderedSet([Roles, Users, Artists, Musics])

CheckTables(models=models).start()

Preload().start()


app.add_url_rule("/", view_func=HealthCheckView.as_view("health_check"))
app.add_url_rule("/register", view_func=RegisterUserView.as_view("register"))
app.add_url_rule("/login", view_func=LoginView.as_view("login"))
