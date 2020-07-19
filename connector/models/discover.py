from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from connector.constants import  AUTH_PROTO_MAP, PRIV_PROTO_MAP, SECURITY_LEVEL_MAPPING

class DiscoverSNMPv2(Schema):
    community = fields.Str(required=True)
    target = fields.Str(required=True)
    version = fields.Str(default="2c")
    timeout = fields.Integer(default=1)
    retries = fields.Integer(default=3)


class DiscoverSNMPv3(Schema):
    auth_key = fields.Str()
    priv_key = fields.Str()
    user = fields.Str()
    usm = fields.Str(validate=OneOf(SECURITY_LEVEL_MAPPING.keys()))
    auth_proto = fields.Str(validate=OneOf(AUTH_PROTO_MAP.keys()))
    priv_proto = fields.Str(validate=OneOf(PRIV_PROTO_MAP.keys()))
    target = fields.Str(required=True)
    version = fields.Str(default="3")
    timeout = fields.Integer(default=1)
    retries = fields.Integer(default=3)