from django.http.response import JsonResponse
from base_app import exceptions

		
class Request:
    def __init__(self, request, method="GET") -> None:
        self.request = request
        if method=="GET":
            self.request = self.request.query_params
        else:
            self.request = self.request.data

    
    def required(self, *args, error_message=None):
        try:
            fields = [self.request[param] for param in args]
        except KeyError:
            raise exceptions.FieldRequired(detail=error_message)
        return tuple(fields)
    
    def opts(self, *args):
        fields = [self.request.get(param) for param in args]
        return tuple(fields)


class Response:
    def __init__(self) -> None:
        self.response = JsonResponse
        self.payload = {
                "status": "Success"
            } 

    def data_response(self, data):
        self.payload["data"] = data
        response = self.response(self.payload)
        return response

    def message_response(self, message):
        self.payload["message"] = message
        response = self.response(self.payload)
        return response
