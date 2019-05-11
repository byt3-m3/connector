from pprint import pprint

from pysnmp.hlapi import *

from app.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP
from app.controllers.handler import Handler
from app.models.snmp_models import SNMPRequest

OID_MAP = {
    "sysDescr": ['SNMPv2-MIB', 'sysDescr', 0],
    "sysName": ['SNMPv2-MIB', 'sysName', 0],
    "cisco_model": ['ENTITY-MIB', 'entPhysicalDescr', 1001]
}


# --- Helper Funcs ----

def _process_v2(community, target, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
                                                                     CommunityData(community, mpModel=0),
                                                                     UdpTransportTarget((target, 161)),
                                                                     ContextData(),
                                                                     ObjectType(
                                                                         ObjectIdentity(*oid))))

    return errorIndication, errorStatus, errorIndex, varBinds


def _process_v3_authpriv(target, v3_user, v3_auth_proto, v3_priv_proto, v3_auth_key, v3_priv_key, oid):
    _authProtocol = AUTH_PROTO_MAP.get(v3_auth_proto, usmNoAuthProtocol)
    _privProtocol = PRIV_PROTO_MAP.get(v3_priv_proto, usmNoPrivProtocol)

    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),

                                                                     UsmUserData(userName=v3_user,
                                                                                 authKey=v3_auth_key,
                                                                                 privKey=v3_priv_key,
                                                                                 authProtocol=_authProtocol,
                                                                                 privProtocol=_privProtocol),
                                                                     UdpTransportTarget((target, 161), timeout=1,
                                                                                        retries=1),
                                                                     ContextData(),
                                                                     ObjectType(ObjectIdentity(*oid))))

    return errorIndication, errorStatus, errorIndex, varBinds


def _process_v3_noauthnopriv(target, v3_user, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
                                                                     UsmUserData(v3_user),
                                                                     UdpTransportTarget((target, 161)),
                                                                     ContextData(),
                                                                     ObjectType(ObjectIdentity(*oid))))

    return errorIndication, errorStatus, errorIndex, varBinds


def _process_v3_authnopriv(target, v3_user, v3_auth_proto, v3_auth_key, oid):
    '''

    This function is used to proces SNMPv3 authnopriv request.

    :param target:
    :param v3_user:
    :param v3_auth_proto:
    :param v3_auth_key:
    :param oid:
    :return:
    '''

    _authProtocol = AUTH_PROTO_MAP.get(v3_auth_proto, usmNoAuthProtocol)

    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
                                                                     UsmUserData(userName=v3_user,
                                                                                 authKey=v3_auth_key,
                                                                                 authProtocol=_authProtocol,
                                                                                 privProtocol=usmNoPrivProtocol),
                                                                     UdpTransportTarget((target, 161)),
                                                                     ContextData(),
                                                                     ObjectType(ObjectIdentity(*oid))))

    return errorIndication, errorStatus, errorIndex, varBinds


# --- SNMPv2 Handlers ---
class SNMPHandler(Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SNMPRequest.validate(kwargs)


class SNMPDevTypeHandler(SNMPHandler):

    def __init__(self, *args, **kwargs):
        """
        This Handler is used to determine device type by using the SNMPv2 protocol.

        This handler uses the SNMPv2 data model for its request validation.
        {
            "community": str,
            "target": str,
            Optional("opts"): dict
        }

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        SNMPRequest.validate(kwargs)
        self.params = kwargs

    def _process_snmp_response(self, errorIndication, errorStatus, errorIndex, varBinds):
        if errorIndication:
            self.response.msg = str(errorIndication)
            self.response.data = str(errorIndication)
            self.response.status = False
            self.response.exception = str(TimeoutError(errorIndication))
            return self.response

        for bind in varBinds:
            data = {}

            if 'Cisco IOS' in str(bind):
                data['node_type'] = "cisco_ios"
                self.response.data = data
                self.response.status = True
                self.response.msg = "Cisco Device Detected"
                return self.response

            if 'Ubuntu' in str(bind):
                data['node_type'] = "linux"
                self.response.data = data
                self.response.status = True
                self.response.msg = "Ubuntu Device Detected"
                return self.response

            if 'Linux' in str(bind):
                data['node_type'] = "linux"
                self.response.data = data
                self.response.status = True
                self.response.msg = "Linux Device Detected"
                return self.response

            data['node_type'] = "undefined"
            self.response.data = data
            self.response.status = True
            self.response.msg = "Unable to determine device type"
            return self.response

    def __call__(self, *args, **kwargs):

        _version = self.params.get("version")
        _target = self.params.get("target")
        _oid = OID_MAP['sysDescr']

        if _version == 2:
            _community = self.params.get("community")

            errorIndication, errorStatus, errorIndex, varBinds = _process_v2(community=_community,
                                                                             target=_target,
                                                                             oid=_oid)

            return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)

        elif _version == 3:
            _v3_usm = self.params.get("v3_usm")
            _v3_sec_models = ['noauthnopriv', 'authnopriv', 'authpriv']

            if _v3_usm == 'noauthnopriv':
                # TODO: Added logic for noauthnopriv
                pass
            elif _v3_usm == 'authnopriv':
                # TODO: Added logic for authnopriv
                _v3_user = self.params.get("v3_user")
                _v3_auth_key = self.params.get("v3_auth_key")
                _v3_auth_proto = self.params.get("v3_auth_proto")
                _v3_priv_key = self.params.get("v3_priv_key")
                _v3_priv_proto = self.params.get("v3_priv_proto")

                errorIndication, errorStatus, errorIndex, varBinds = _process_v3_authnopriv(target=_target,
                                                                                            v3_user=_v3_user,
                                                                                            v3_auth_key=_v3_auth_key,
                                                                                            v3_auth_proto=_v3_auth_proto,

                                                                                            oid=_oid)

                return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)
            elif _v3_usm == 'authpriv':

                _v3_user = self.params.get("v3_user")
                _v3_auth_key = self.params.get("v3_auth_key")
                _v3_auth_proto = self.params.get("v3_auth_proto")
                _v3_priv_key = self.params.get("v3_priv_key")
                _v3_priv_proto = self.params.get("v3_priv_proto")

                errorIndication, errorStatus, errorIndex, varBinds = _process_v3_authpriv(target=_target,
                                                                                          v3_user=_v3_user,
                                                                                          v3_auth_key=_v3_auth_key,
                                                                                          v3_auth_proto=_v3_auth_proto,
                                                                                          v3_priv_key=_v3_priv_key,
                                                                                          v3_priv_proto=_v3_priv_proto,
                                                                                          oid=_oid)

                return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)


class SNMPHostnameHandler(SNMPHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SNMPRequest.validate(kwargs)
        self.params = kwargs

    def _process_snmp_response(self, errorIndication, errorStatus, errorIndex, varBinds):
        if errorIndication:
            self.response.msg = str(errorIndication)
            self.response.data = str(errorIndication)
            self.response.status = False
            self.response.exception = str(TimeoutError(errorIndication))
            return self.response

        for bind in varBinds:
            data = {}
            data['hostname'] = bind.prettyPrint().replace("SNMPv2-MIB::sysName.0 = ", "")
            self.response.data = data
            return self.response

    def __call__(self, *args, **kwargs):

        _version = self.params.get("version")
        _target = self.params.get("target")
        _oid = OID_MAP['sysName']

        if _version == 2:
            _community = self.params.get("community")

            errorIndication, errorStatus, errorIndex, varBinds = _process_v2(community=_community,
                                                                             target=_target,
                                                                             oid=_oid)

            return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)

        elif _version == 3:
            _v3_usm = self.params.get("v3_usm")
            _v3_sec_models = ['noauthnopriv', 'authnopriv', 'authpriv']

            if _v3_usm == 'noauthnopriv':
                # TODO: Added logic for noauthnopriv
                pass
            elif _v3_usm == 'authnopriv':
                # TODO: Added logic for authnopriv
                _v3_user = self.params.get("v3_user")
                _v3_auth_key = self.params.get("v3_auth_key")
                _v3_auth_proto = self.params.get("v3_auth_proto")
                _v3_priv_key = self.params.get("v3_priv_key")
                _v3_priv_proto = self.params.get("v3_priv_proto")

                errorIndication, errorStatus, errorIndex, varBinds = _process_v3_authnopriv(target=_target,
                                                                                            v3_user=_v3_user,
                                                                                            v3_auth_key=_v3_auth_key,
                                                                                            v3_auth_proto=_v3_auth_proto,

                                                                                            oid=_oid)

                return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)

            elif _v3_usm == 'authpriv':

                _v3_user = self.params.get("v3_user")
                _v3_auth_key = self.params.get("v3_auth_key")
                _v3_auth_proto = self.params.get("v3_auth_proto")
                _v3_priv_key = self.params.get("v3_priv_key")
                _v3_priv_proto = self.params.get("v3_priv_proto")

                errorIndication, errorStatus, errorIndex, varBinds = _process_v3_authpriv(target=_target,
                                                                                          v3_user=_v3_user,
                                                                                          v3_auth_key=_v3_auth_key,
                                                                                          v3_auth_proto=_v3_auth_proto,
                                                                                          v3_priv_key=_v3_priv_key,
                                                                                          v3_priv_proto=_v3_priv_proto,
                                                                                          oid=_oid)

                return self._process_snmp_response(errorIndication, errorStatus, errorIndex, varBinds)


def test_snmpv2():
    errorIndication, errorStatus, errorIndex, varBinds = next(getCmd(SnmpEngine(),
                                                                     CommunityData("bits_rw", mpModel=0),
                                                                     UdpTransportTarget(("192.168.1.2", 161)),
                                                                     ContextData(),
                                                                     ObjectType(
                                                                         ObjectIdentity(
                                                                             *OID_MAP['cisco_model']).addMibSource(
                                                                             "C:\\Users\\cbaxt\\Documents\\code\\python\\app\\app\\mibs"))))

    for bind in varBinds:
        print(bind)


def test_snmpv2_walk():
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData("bits_rw", mpModel=0),
                              UdpTransportTarget(('192.168.1.2', 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity('ENTITY-MIB', 'entPhysicalDescr', 1001).addMibSource(
                                  "C:\\Users\\cbaxt\\Documents\\code\\python\\app\\app\\mibs"))):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))


def test_snmpv2_host_discover_handler():
    data = {
        "method": "snmpv2_host",
        "params": {
            "community": "bits_rw",
            "target": "192.168.1.9"
        },
        "opts": {},
        "filters": {}
    }

    handler = SNMPDevTypeHandler(**data)

    result = handler()
    print(result)


def test_snmpv2_network_discover_handler():
    data = {
        "method": "snmpv2_network",
        "params": {
            "community": "bits_rw",
            "target": "192.168.1.0/29"
        },
        "opts": {},
        "filters": {}
    }

    handler = SNMPDevTypeHandler(**data)
    pprint(handler())


if __name__ == '__main__':
    test_snmpv2_host_discover_handler()
    test_snmpv2_network_discover_handler()
