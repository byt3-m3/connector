from flask import Flask, render_template
from flask_restful import Api

# --- App Imports ---
from app.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP, V3_SEC_MODELS, DEV_TYPES
from app.controllers.dispatch import HANDLER_MAP
from app.resources.access import AccessResource
from app.resources.discover import DiscoverResource

app = Flask(__name__)
api = Api(app)

api.add_resource(DiscoverResource, "/api/v1/discover")
api.add_resource(AccessResource, "/api/v1/access")


@app.route("/test_snmp", methods=['GET', 'POST'])
def test_snmp():
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
