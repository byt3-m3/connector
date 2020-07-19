from flask import Flask, render_template
from flask_restful import Api
from connector.exceptions import *

# --- App Imports ---
from connector.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP, DEV_TYPES, SECURITY_LEVEL_MAPPING
from connector.controllers.dispatch import HANDLER_MAP
from connector.resources import (
    DiscoverSNMPv3,
    DiscoverSNMPv2
)


app = Flask(__name__)
api = Api(app)

api.add_resource(DiscoverSNMPv2, "/api/v1/discover/snmp/v2c", endpoint="post")
api.add_resource(DiscoverSNMPv3, "/api/v1/discover/snmp/v3")



@app.route("/test/access", methods=['GET', 'POST'])
def test_access():
    AUTH_PROTO_OPTS = list(AUTH_PROTO_MAP.keys())
    PRIV_PROTO_OPTS = list(PRIV_PROTO_MAP.keys())
    METHOD_OPTS = list(HANDLER_MAP.keys())
    SEC_MODELS = SECURITY_LEVEL_MAPPING.keys()

    return render_template("test_snmp.j2",
                           auth_protos=AUTH_PROTO_OPTS,
                           priv_protos=PRIV_PROTO_OPTS,
                           sec_models=SEC_MODELS,
                           node_types=DEV_TYPES,
                           methods=METHOD_OPTS)
