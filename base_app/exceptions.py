from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, NotFound


class TokenExpired(APIException):
    status_code = 401
    default_detail = 'Your token has expired.'
    default_code = 'token expired'


class InvalidToken(APIException):
    status_code = 401
    default_detail = 'Your token is invalid.'
    default_code = 'token invalid'
    

class WrongPassword(APIException):
    status_code = 401
    default_detail = 'Wrong password'
    default_code = 'forbidden'
    

class DisbandedUserResponse(APIException):
    status_code = 403
    default_detail = 'Your are not allowed to do this. If this is a mistake, please contact an administrator'
    default_code = 'unauthorized'
    

class WrongFieldType(APIException):
    status_code = 400
    default_detail = 'Wrong field type provided'
    default_code = 'bad request'
    

class FieldRequired(APIException):
    status_code = 400
    default_detail = 'Missing Field Required'
    default_code = 'bad request'


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    response.data['status'] = "Error"
    response.data['message'] = response.data.pop('detail')

    return response