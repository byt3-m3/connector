from flask import Response, request
from flask_restful import Resource, fields
from app.constants import (JSON_RESPONSE_HEADERS,
                           STATUS_201_CREATED,
                           STATUS_417_EXPECTATION_FAILED,
                           STATUS_200_SUCCESS,
                           STATUS_400_BAD_REQUEST)

request_model = {
    "method": fields.String(default="snmpv2HostDiscovery"),
    "params": fields.Nested(nested={}),
    "opts": fields.Nested(nested={}),
    "filters": fields.Nested(nested={})
}


