from connector.models import DiscoverSNMPv2, DiscoverSNMPv3
from connector.constants import MIB_MAP
from connector.controllers.core import ControllerResult, validate_params
from connector.controllers.snmp_client import SNMPV3Client, SNMPV2Client
import re


def _update_node_type(facts, sysDescr):
    if "Cisco IOS" in sysDescr:
        facts['node_type'] = "cisco_ios"

    if "Linux" in sysDescr:
        facts['node_type'] = "linux"

    return facts


def _update_sys_name(facts, sysName):
    PATTERN = re.compile('SNMPv2-MIB::sysName.0 = (.*)')

    match = PATTERN.findall(sysName)
    if len(match) == 1:
        facts['assetHostname'] = match.pop()


def _get_node_facts(client):
    facts = {}

    result = client.get(MIB_MAP.get("sysDescr"))
    if isinstance(result, dict):
        if result.get("errorIndication"):
            return ControllerResult(data=None, result=False, msg=f"ERROR: {client.host} unreachable", status=409)

        if result.get("varBinds"):
            for var in result.get("varBinds"):
                sys_description = var.prettyPrint()

                _update_node_type(facts, sys_description)

    result = client.get(MIB_MAP.get("sysName"))
    if isinstance(result, dict):
        if result.get("errorIndication"):
            return ControllerResult(data=None, result=False, msg=f"ERROR: {client.host} unreachable", status=409)

        if result.get("varBinds"):
            for var in result.get("varBinds"):
                sysName = var.prettyPrint()

                _update_sys_name(facts, sysName)

    return ControllerResult(data=facts, result=True, msg="Successful", status=200)


def controller_discover_snmpv3(params):
    result = validate_params(DiscoverSNMPv3, params)

    if result.status != 200:
        return result

    usm = params.get("usm")
    user = params.get("user")
    auth_key = params.get("auth_key")
    priv_key = params.get("priv_key")
    auth_proto = params.get("auth_proto")
    priv_proto = params.get("priv_proto")

    host = params.get("target")
    timeout = params.get("timeout", 1)
    retries = params.get("retries", 2)

    snmp_client = SNMPV3Client(host=host,
                               timeout=timeout,
                               retries=retries,
                               usm=usm,
                               user=user,
                               auth_key=auth_key,
                               priv_key=priv_key,
                               auth_proto=auth_proto,
                               priv_proto=priv_proto
                               )

    return _get_node_facts(snmp_client)


def controller_discover_snmpv2(params):
    result = validate_params(DiscoverSNMPv2, params)
    if result.status != 200:
        return result

    host = params.get("target")
    community = params.get("community")
    timeout = params.get("timeout", 1)
    retries = params.get("retries", 2)

    snmp_client = SNMPV2Client(host=host, community=community, retries=retries, timeout=timeout)

    return _get_node_facts(snmp_client)
