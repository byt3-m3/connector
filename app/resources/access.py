from app.controllers.dispatch import Dispatcher
from app.models.api_models import APIRequestSchema
from app.tools import APIResponse
from . import Resource, request, STATUS_200_SUCCESS, STATUS_400_BAD_REQUEST


class AccessResource(Resource):
    @staticmethod
    def post():

        request_json = request.json

        if not APIRequestSchema.is_valid(request_json):
            print(APIRequestSchema.validate(request_json))
            return APIResponse(data=None, msg="Invalid API Request", status=STATUS_400_BAD_REQUEST)()

        # Dispatches the request of the appropriate handler and executes Handlers __call__() method
        dispatcher = Dispatcher()
        results = dispatcher.dispatch(request_json)
        # results = handler()


        if results.exception:

            return APIResponse(data=results.msg, exception=str(results.exception), status=STATUS_400_BAD_REQUEST)()

        if results:
            # print(results)
            return APIResponse(data=results.data, status=STATUS_200_SUCCESS)()

        # --- Returns if no conditions are met. ---
        return APIResponse(data=None, msg="No Conditions Met: Unknown Error", status=STATUS_200_SUCCESS)()
