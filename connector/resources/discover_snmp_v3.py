from flask_restful import Resource
from flask import request
from connector.controllers.discover_snmp import controller_discover_snmpv3, ControllerResult
from connector.utils import make_json_response


class DiscoverSNMPv3(Resource):

    def post(self):
        params = request.json

        result = controller_discover_snmpv3(params)
        if isinstance(result, ControllerResult):
            return make_json_response(result.data, result.msg, result.status)
        else:
            return make_json_response(None, "Unknown Error Encountered", 400)
