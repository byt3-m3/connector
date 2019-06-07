from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException

from app.constants import DEV_TYPES
from app.controllers.handler import Handler
from app.models.ssh_models import SSHCMDRequestSchema


def get_ssh_connector(kwargs):
    _device_type = kwargs.get("device_type") if kwargs.get("device_type") in DEV_TYPES else "cisco_ios"
    ssh_passwd = kwargs.get("password")

    connector_data = {'device_type': _device_type,
                      'username': kwargs.get("username"),
                      'password': ssh_passwd,
                      'secret': kwargs.get("secret", ssh_passwd),
                      'host': kwargs.get("host")}

    return ConnectHandler(**connector_data)


class SSHHandler(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SSHCMDRequestSchema.validate(kwargs)

        self.params = {
            'device_type': kwargs.get("node_type") if kwargs.get("node_type") in DEV_TYPES else "cisco_ios",
            'username': kwargs.get("ssh_username"),
            'password': kwargs.get("ssh_password"),
            'secret': kwargs.get("ssh_enable", kwargs.get("ssh_password")),
            'host': kwargs.get("target"),
            'cmd': kwargs.get("cmd")
        }

    def __call__(self, *args, **kwargs):
        try:
            self.con_obj = get_ssh_connector(self.params)
        except NetMikoTimeoutException as err:

            self.response.exception = err
            self.response.status = False
            self.response.msg = f'Connection timeout to {self.params["host"]}'
            return self.response

        # checks if the device in privilege mode, if not enter enable mode.
        if not self.con_obj.check_enable_mode():
            self.con_obj.enable()

        try:
            command_result = self.con_obj.send_command(self.params['cmd'])

            # self.response.data = self.con_obj.send_command(self.params['cmd'])
            self.con_obj.disconnect()
            self.response.status = True

            _response_type = self.opts.get("response_type", 'str')

            if _response_type == 'list':
                self.response.data = command_result.split("\n")

            if _response_type == 'str':
                self.response.data = command_result

            return self.response

        except NetMikoTimeoutException as err:
            self.response.exception = err
            self.response.status = False
            self.response.msg = f'Could not connection to {self.params["target"]})'
            return self.response


# TODO: Create SSHConfig Handler

