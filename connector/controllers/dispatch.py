from .handler import UnknownTypeHandler, Handler
from .snmp_handlers import SNMPDevTypeHandler, SNMPHostnameHandler
from .ssh_handlers import SSHHandler

HANDLER_MAP = {
    "snmp_devtype": SNMPDevTypeHandler,
    "snmp_hostname": SNMPHostnameHandler,
    "ssh_cmd": SSHHandler
}


class Dispatcher:

    def __init__(self, *args, **kwargs):

        self.method = None
        self.data = None

    def dispatch(self, data):
        _method = data.get("method")
        _params = data.get("params")
        _opts = data.get("opts")

        _handler = HANDLER_MAP.get(_method, UnknownTypeHandler)(**_params, opts=_opts)

        if isinstance(_handler, UnknownTypeHandler):
            return _handler(method=_method)

        if isinstance(_handler, Handler):
            return _handler()
        else:
            return None
