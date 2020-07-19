from flask_restful import Resource
from flask import request
from connector.controllers import controller_discover_snmpv2, ControllerResult
from connector.utils import make_json_response


class DiscoverSNMPv2(Resource):

    def post(self):
        params = request.json

        c_result = controller_discover_snmpv2(params)
        if isinstance(c_result, ControllerResult):
            return make_json_response(data=c_result.data, msg=c_result.msg, status_code=c_result.status)
        else:
            return make_json_response(data=None, msg="Unknown Error Occured", status_code=400)