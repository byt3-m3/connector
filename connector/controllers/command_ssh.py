from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from connector.controllers.core import ControllerResult, validate_params
from connector.models.command_ssh import SSHCommandSchema
from connector.constants import DEV_TYPES


def _get_ssh_handler(kwargs):
    _device_type = kwargs.get("node_type") if kwargs.get("node_type") in DEV_TYPES else "cisco_ios"
    ssh_passwd = kwargs.get("password")
    print(_device_type)
    connector_data = {'device_type': _device_type,
                      'username': kwargs.get("username"),
                      'password': ssh_passwd,
                      'secret': kwargs.get("secret", ssh_passwd),
                      'host': kwargs.get("target")}

    return ConnectHandler(**connector_data)


def controller_ssh_cmd(params):

    result = validate_params(SSHCommandSchema, params)
    if result.status != 200:
        return result
    cmd = params.get("cmd")

    try:
        print("HJand")
        handler = _get_ssh_handler(params)
        results = handler.send_command(cmd)
        print(results)
    except NetMikoTimeoutException as err:
        return ControllerResult(None, False, f"ERROR: {str(err)}", 504)

    except Exception:
        raise

    return ControllerResult(results, True, "Successful", 200)



def controller_ssh_cmds(params):

    result = validate_params(SSHCommandSchema, params)
    if result.status != 200:
        return result
    cmds = params.get("cmds")

    try:
        handler = _get_ssh_handler(params)
        cmd_results = []
        for cmd in cmds:
            results = handler.send_command(cmd)
            cmd_results.append(results)

    except NetMikoTimeoutException as err:
        return ControllerResult(None, False, f"ERROR: {str(err)}", 504)

    return ControllerResult(cmd_results, True, "Successful", 200)

