from base_app import http
from main_app.auth import UserAuth 
from main_app.repository import AccountRepository


class SignInController:
    def __init__(self, **kwargs) -> None:
        self.requests = http.Request
        self.responses = http.Response()
        self.auth = UserAuth()
        self.repo = AccountRepository()

    def signin(self, request):
        query = self.requests(request, method="POST")
        email, password = query.required(
            "email", "password", 
            error_message="Email and password are required!"
            )
        
        auth = self.auth.check_account(email, password).gen_token_from_account()
        payload = {
            "accessToken": auth.token
        }
        return self.responses.data_response(payload)

    def update_password(self, request):
        query = self.requests(request, method='PUT')
        password, = query.required("password", error_message="Password is required")

        user = self.repo.update_password(
            account=request.user, 
            password=password
        )

        return self.responses.message_response(
            message = f"{user.first_name} your password has been changed successfully."
        )
       