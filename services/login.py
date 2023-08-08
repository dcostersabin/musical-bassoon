from db.crud import CRUDBase
from models.users import Users
from werkzeug.security import check_password_hash


class LoginService:
    def __init__(self, data: dict):
        self.data = data
        self.user = None

    def login(self) -> bool:
        return self.verify()

    def verify(self) -> bool:
        curd_obj = CRUDBase(model=Users)
        user = curd_obj.filter(data={"email": self.data.get("email")})
        if len(user) == 0:
            return False

        user = user[0]
        self.user = user

        return check_password_hash(
            user.get("password", "n/A"), self.data.get("password", "")
        )
