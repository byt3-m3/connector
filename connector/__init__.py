from flask import Flask, render_template
from flask_restful import Api
from connector.exceptions import *

# --- App Imports ---
from connector.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP, V3_SEC_MODELS, DEV_TYPES
from connector.controllers.dispatch import HANDLER_MAP
from connector.resources.access import AccessResource
from connector.resources.discover import DiscoverResource

app = Flask(__name__)
api = Api(app)

api.add_resource(DiscoverResource, "/api/v1/discover")
api.add_resource(AccessResource, "/api/v1/access")


@app.route("/test/access", methods=['GET', 'POST'])
def test_access():
    AUTH_PROTO_OPTS = list(AUTH_PROTO_MAP.keys())
    PRIV_PROTO_OPTS = list(PRIV_PROTO_MAP.keys())
    METHOD_OPTS = list(HANDLER_MAP.keys())
    SEC_MODELS = V3_SEC_MODELS

    return render_template("test_snmp.j2",
                           auth_protos=AUTH_PROTO_OPTS,
                           priv_protos=PRIV_PROTO_OPTS,
                           sec_models=SEC_MODELS,
                           node_types=DEV_TYPES,
                           methods=METHOD_OPTS)
