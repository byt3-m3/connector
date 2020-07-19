from flask_restful import Resource
from flask import request
from connector.controllers.command_ssh import controller_ssh_cmd, ControllerResult, controller_ssh_cmds
from connector.utils import make_json_response


class SSHCommand(Resource):

    def post(self):
        params = request.json
        opts = request.args
        return_type = opts.get("return_type", "list")

        if params.get("cmd"):

            result = controller_ssh_cmd(params)
            if isinstance(result, ControllerResult):
                if return_type == "string":
                    return make_json_response(result.data, result.msg, result.status)

                else:
                    return make_json_response(result.data.split("\n"), result.msg, result.status)

        if params.get("cmds"):

            c_result = controller_ssh_cmds(params)

            if isinstance(c_result, ControllerResult):
                if return_type == "string":

                    return make_json_response(c_result.data, c_result.msg, c_result.status)

                else:
                    res = [result.split("\n") for result in c_result.data]

                return make_json_response(res, c_result.msg, c_result.status)
