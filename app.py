from flask import Flask
from config import get_config
from models.users import Users
from models.musics import Musics
from models.roles import Roles
from ordered_set import OrderedSet
from db.models.check import CheckTables
from flask_cors import CORS
from preload import Preload
from views import HealthCheckView
from views.register import RegisterUserView
from views.login import LoginView
from views.users import UserView
from views.music import MusicView
from views.profile import ProfileView
from views.dump_data import DumpDataView
from views.upload_music import UploadMusicView
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)

config = get_config()
app.config.from_object(config)

models = OrderedSet([Roles, Users, Musics])

CheckTables(models=models).start()

Preload().start()


app.add_url_rule("/", view_func=HealthCheckView.as_view("health_check"))
app.add_url_rule("/register", view_func=RegisterUserView.as_view("register"))
app.add_url_rule("/login", view_func=LoginView.as_view("login"))
app.add_url_rule("/users", view_func=UserView.as_view("user"))
app.add_url_rule("/music", view_func=MusicView.as_view("music"))
app.add_url_rule("/dump", view_func=DumpDataView.as_view("dump"))
app.add_url_rule("/profile", view_func=ProfileView.as_view("profile"))
app.add_url_rule("/upload", view_func=UploadMusicView.as_view("upload"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
