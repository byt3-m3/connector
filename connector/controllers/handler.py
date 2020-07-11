from netmiko import ConnectHandler
from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE

from connector.exceptions import InvalidTypeError

DEV_TYPES = iter(CLASS_MAPPER_BASE.keys())


def get_ssh_connector(node_data: dict):
    _device_type = node_data.get("node_type")
    ssh_passwd = node_data.get("ssh_password")
    connector_data = {'device_type': _device_type if _device_type in DEV_TYPES else "cisco_ios",
                      'username': node_data.get("ssh_username"),
                      'password': ssh_passwd,
                      'secret': node_data.get("ssh_enable", ssh_passwd),
                      'host': node_data.get("ip")}


    return ConnectHandler(**connector_data)


class Handler(object):
    def __init__(self, *args, **kwargs):
        self.response = HandlerResponse()
        self.params = kwargs.get("params")

        self.opts = kwargs.get("opts")


    def __call__(self, *args, **kwargs):
        """
        Implement Handler functionality.

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def __dict__(self):
        return self._model

    def __iter__(self):
        for k, v in self._model.items():
            yield k, v


class HandlerResponse(object):
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get("data")
        self.exception = kwargs.get("exception")
        self.msg = kwargs.get("msg")
        self.status = kwargs.get("status", False)

    def __repr__(self):
        return f"<connector.handlers.handler.HandlerResponse(status={self.status}, msg={self.msg}, data={self.data}, exception={self.exception})>"

    def __dict__(self):
        return {
            "data": self.data,
            "msg": self.msg,
            "exception": self.exception,
            "status": self.status
        }


class UnknownTypeHandler(Handler):
    def __init__(self, *args, **kwargs):
        """
        This Handler is used to Handle Unknown Method types.
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.response.data = f'No Handler found for: {kwargs.get("method", "Unknown Method")}'
        self.response.exception = InvalidTypeError()
        return self.response
