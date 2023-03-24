from datetime import datetime, timedelta
import jwt
from django.db.models import Model
from django.contrib.auth.hashers import check_password
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from base_app import http
from base_app import exceptions 
from base_app.base_repo import BaseRepo

class BaseAuth(BaseAuthentication):
    def __init__(self) -> None:
        super().__init__()
        self.jwt = jwt
        self.request = http.Request
        self.response = http.Response()
        self.model = Model
        self.repo = BaseRepo()
        self.identifier = 'id'
        self.login_protocol = "email"
        self.login_protocol_mismatch_msg = "Wrong email, please check and try again"

    def check_account(self, email = None, password = None):
        if email and password:
            try:
                account = self.repo.get_by_keyword({self.login_protocol: email})
            except self.model.DoesNotExist:
                raise exceptions.NotFound(self.login_protocol_mismatch_msg)
            if not check_password(password, account.password):
                raise exceptions.WrongPassword()
        else:
            account = self.repo.get_by_keyword({self.identifier: self.account_ID})
        if account.is_authenticated:
            self.account = account
        else:
            raise exceptions.DisbandedUserResponse
        return self

    def gen_token_from_account(self, account = None, exp_time=8):
        if account is None:
            account = self.account
        payload = {
            "ID": getattr(account, self.identifier),
            "exp": datetime.utcnow() + timedelta(hours=exp_time)
        }
        token = self.jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm=settings.CRYPTOGRAPHIC_ALGORITHM
        )
        self.token = token
        return self

    def get_accountID_from_token(self, token = None):
        if token is None:
            token = self.token
        try:
            payload = self.jwt.decode(
                token,
                key=settings.SECRET_KEY,
                algorithms=[settings.CRYPTOGRAPHIC_ALGORITHM]
            )
        except self.jwt.exceptions.ExpiredSignatureError:
            raise exceptions.TokenExpired
        except self.jwt.exceptions.InvalidTokenError:
            raise exceptions.InvalidToken
        self.account_ID = payload.get("ID")
        return self

    def authenticate(self, request):
        try:
            authorization = request.headers["authorization"]
        except KeyError:
            raise exceptions.FieldRequired("An authorization key in header is required")
        [*_, token] = authorization.split()
        auth = self.get_accountID_from_token(token).check_account()
        return auth.account, token
        