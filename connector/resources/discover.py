import json

from connector.utils import APIResponse
from connector.controllers.dispatch import Dispatcher
from . import Resource, Response, request, JSON_RESPONSE_HEADERS, STATUS_200_SUCCESS, STATUS_400_BAD_REQUEST
from connector.controllers.handler import HandlerResponse

class DiscoverResource(Resource):

    def post(self, **kwargs):
        handler_factory = Dispatcher()

        data = request.json
        handler = handler_factory.dispatch(data)

        results = handler()
        response = {"response": "", "msg": "", "exception": None}

        if results.exception:
            return Response(json.dumps(response), headers=JSON_RESPONSE_HEADERS, status=STATUS_400_BAD_REQUEST)

        if not results:
            return Response(json.dumps(response), headers=JSON_RESPONSE_HEADERS, status=STATUS_400_BAD_REQUEST)

        if isinstance(results, HandlerResponse):
            response['response'] = results.data
            response['msg'] = results.msg

            return APIResponse(data=response, status=STATUS_200_SUCCESS)()
            # return Response(json.dumps(response), headers=JSON_RESPONSE_HEADERS, status=STATUS_200_SUCCESS)
