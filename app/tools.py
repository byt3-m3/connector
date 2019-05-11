import json

from flask import Response

JSON_RESPONSE_HEADERS = {'content-type': 'application/json; charset=utf-8'}


class APIResponse:

    def __init__(self, data=None, msg=None, status=404, exception=None):
        self.data = data
        self.msg = msg
        self.exception = exception
        self.status = status

    def __call__(self, *args, **kwargs):
        response = {"response": self.data, "msg": self.msg, "exception": self.exception}

        return Response(json.dumps(response), headers=JSON_RESPONSE_HEADERS, status=self.status)
