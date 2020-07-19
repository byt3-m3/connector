from pysnmp.hlapi import *
from connector.constants import AUTH_PROTO_MAP, PRIV_PROTO_MAP


class SNMPClient:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host")
        self.port = kwargs.get("port", 161)
        self.timeout = kwargs.get("timeout", 1)
        self.retries = kwargs.get("retries")

        self.engine = SnmpEngine()
        self._transport_object = UdpTransportTarget((self.host, self.port), self.timeout, self.retries)


class SNMPV2Client(SNMPClient):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.community = kwargs.get("community")

        self._community_obj = CommunityData(self.community)

    def get(self, oid):
        oid_obj = ObjectType(ObjectIdentity(oid))
        results = []

        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(self.engine, self._community_obj, self._transport_object, ContextData(), oid_obj):
            results.append(
                {
                    "errorIndication": errorIndication,
                    "errorStatus": errorStatus,
                    "errorIndex": errorIndex,
                    "varBinds": varBinds
                }
            )

        if len(results) == 1:
            return results.pop()
        else:
            return results


class SNMPV3Client(SNMPV2Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = kwargs.get("user")
        self.auth_key = kwargs.get("auth_key")
        self.auth_proto = kwargs.get("auth_proto", "none")
        self.priv_proto = kwargs.get("priv_proto", "none")
        self.usm = kwargs.get("usm", "noAuthNoPriv")
        self.target = kwargs.get("target")
        self.priv_key = kwargs.get("priv_key")

    def get(self, oid):
        _authProtocol = AUTH_PROTO_MAP.get(self.auth_proto, usmNoAuthProtocol)
        _privProtocol = PRIV_PROTO_MAP.get(self.priv_proto, usmNoPrivProtocol)
        oid_obj = ObjectType(ObjectIdentity(oid))
        results = []

        if self.usm == "authPriv":
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in getCmd(self.engine,
                                     UsmUserData(userName=self.user,
                                                 authKey=self.auth_key,
                                                 privKey=self.priv_key,
                                                 authProtocol=_authProtocol,
                                                 privProtocol=_privProtocol),
                                     UdpTransportTarget((self.host, 161), timeout=self.timeout,
                                                        retries=self.retries),
                                     ContextData(),
                                     oid_obj):
                results.append(
                    {
                        "errorIndication": errorIndication,
                        "errorStatus": errorStatus,
                        "errorIndex": errorIndex,
                        "varBinds": varBinds
                    }
                )

        if self.usm == "authNoPriv":
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in getCmd(self.engine,
                                     UsmUserData(userName=self.user,
                                                 authKey=self.auth_key,
                                                 authProtocol=_authProtocol,
                                                 privProtocol=usmNoPrivProtocol),
                                     UdpTransportTarget((self.host, 161), timeout=self.timeout,
                                                        retries=self.retries),
                                     ContextData(),
                                     oid_obj):
                results.append(
                    {
                        "errorIndication": errorIndication,
                        "errorStatus": errorStatus,
                        "errorIndex": errorIndex,
                        "varBinds": varBinds
                    }
                )

        if self.usm == "noAuthNoPriv":
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in getCmd(self.engine,
                                     UsmUserData(userName=self.user,
                                                 authProtocol=usmNoAuthProtocol,
                                                 privProtocol=usmNoPrivProtocol),
                                     UdpTransportTarget((self.host, 161), timeout=self.timeout,
                                                        retries=self.retries),
                                     ContextData(),
                                     oid_obj):
                results.append(
                    {
                        "errorIndication": errorIndication,
                        "errorStatus": errorStatus,
                        "errorIndex": errorIndex,
                        "varBinds": varBinds
                    }
                )

        if len(results) == 1:
            return results.pop()
        else:
            return results
