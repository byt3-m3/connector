import json


def validate_params(schema, params):
    schema = schema()
    validation_result = schema.validate(params)
    if validation_result:
        return ControllerResult(data=None, result=False, msg=f"Invalid Params: {validation_result}", status=406)
    else:
        return ControllerResult(data=None, result=True, msg=f"Validation Success", status=200)


class ControllerResult:
    def __init__(self, data: object, result: bool, msg: str, status: int = 0):
        self.result = result
        self.msg = msg
        self.data = data
        self.status = status

    @staticmethod
    def new(data: object, result: bool, msg: str, status: int = 0):
        return ControllerResult(data, result, msg, status)

    def to_json(self):
        return json.dumps({
            "result": self.result,
            "msg": self.msg,
            "data": self.data,
            "status": self.status,

        })
