from base_app.models import User
from base_app.base_repo import BaseRepo


class AccountRepository(BaseRepo):
    def __init__(self) -> None:
        super().__init__()
        self.model = User
        self.model_objects = self.model.objects
        
    def update_password(self, account, password):
        account.password = password
        account.save()
        return account