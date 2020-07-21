from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Range

from connector.constants import DEV_TYPES


class SSHCommandSchema(Schema):
    node_type = fields.Str(required=True, validate=OneOf(DEV_TYPES))
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    cmd = fields.Str()
    cmds = fields.List(fields.Str())
    target = fields.Str(required=True)
    ssh_priv_key = fields.Str()
    ssh_pub_key = fields.Str()
    timeout = fields.Int(validate=Range(min=1, max=100))
    retries = fields.Int(validate=Range(min=1, max=20))
