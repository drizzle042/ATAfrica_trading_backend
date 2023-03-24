from rest_framework.views import APIView
from main_app.auth import UserAuth
from main_app.controllers.signin import SignInController


class ProtectedView(APIView):
    authentication_classes = [UserAuth]


class SigninView(APIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.controller = SignInController()
    
    def post(self, request):
        return self.controller.signin(request)
    