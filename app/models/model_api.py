from app.models import request_pb2
from app.models.model_protobuf import ProtobuffModelBase


class APIRequestModel(ProtobuffModelBase):

    def __init__(self, *args, **kwargs):
        super(APIRequestModel, self).__init__(*args, **kwargs, message=request_pb2.APIRequest())




def test_api_request_model():

    req = {
        "method": "ssh_cmd",
        "params": {"mgmtIp": "10.0.0.1"},
        "opts": {}
    }
    a = APIRequestModel()
    a.update(req)

    print(a.to_dict())
   

test_api_request_model()