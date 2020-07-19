from marshmallow import Schema, fields


class SSHCommandSchema(Schema):
    node_type = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    cmd = fields.Str()
    cmds = fields.List(fields.Str())
    target = fields.Str(required=True)
    ssh_priv_key = fields.Str()
    ssh_pub_key = fields.Str()
    timeout = fields.Int()
    retries = fields.Int()
