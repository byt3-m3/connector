from flask import Flask, render_template
from flask_restful import Api
from connector.exceptions import *

# --- App Imports ---
from connector.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP, DEV_TYPES, SECURITY_LEVEL_MAPPING
from connector.resources import (
    DiscoverSNMPv3,
    SSHCommand,
    DiscoverSNMPv2
)

app = Flask(__name__)
api = Api(app)

api.add_resource(DiscoverSNMPv2, "/api/v1/discover/snmp/v2c", endpoint="post")
api.add_resource(DiscoverSNMPv3, "/api/v1/discover/snmp/v3")
api.add_resource(SSHCommand, "/api/v1/command/ssh")


