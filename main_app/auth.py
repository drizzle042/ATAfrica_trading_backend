from base_app.base_auth import BaseAuth
from base_app.models import User
from main_app.repository import AccountRepository

class UserAuth(BaseAuth):
    def __init__(self) -> None:
        super().__init__()
        self.model = User
        self.repo = AccountRepository()
        