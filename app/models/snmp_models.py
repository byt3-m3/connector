from . import Schema, Optional
from app.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP, usmNoAuthProtocol, usmNoPrivProtocol, V3_SEC_MODELS

_snmp_versions = [1, 2, 3]

SNMPRequest = Schema({
    Optional("community"): str,
    Optional("v3_auth_key"): str,
    Optional("v3_priv_key"): str,
    Optional("v3_user"): str,
    Optional("v3_usm"): lambda a: a in V3_SEC_MODELS,
    Optional("v3_auth_proto"): lambda a: AUTH_PROTO_MAP.get(a, usmNoAuthProtocol),
    Optional("v3_priv_proto"): lambda a: PRIV_PROTO_MAP.get(a, usmNoPrivProtocol),
    "target": str,
    "version": lambda a: a in _snmp_versions,
    Optional("opts"): dict

})
