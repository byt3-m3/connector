from netmiko.ssh_dispatcher import CLASS_MAPPER_BASE
from pysnmp.hlapi import (usmNoPrivProtocol,
                          usmAesCfb128Protocol,
                          usmHMACMD5AuthProtocol,
                          usmHMACSHAAuthProtocol,
                          usmHMAC128SHA224AuthProtocol,
                          usmHMAC192SHA256AuthProtocol,
                          usmHMAC256SHA384AuthProtocol,
                          usmHMAC384SHA512AuthProtocol,
                          usmNoAuthProtocol,
                          usmDESPrivProtocol,
                          usm3DESEDEPrivProtocol,
                          usmAesCfb192Protocol,
                          usmAesCfb256Protocol)

# --- APP Constants ---
JSON_RESPONSE_HEADERS = {'content-type': 'application/json; charset=utf-8'}

STATUS_417_EXPECTATION_FAILED = 417
STATUS_400_BAD_REQUEST = 400
STATUS_200_SUCCESS = 200
STATUS_201_CREATED = 201
SNMP_TIMEOUT = 5
SSH_TIMEOUT = 5

# --- SNMP Constants ---
AUTH_PROTO_MAP = {
    "hmac_md5": usmHMACMD5AuthProtocol,
    "hmac_sha": usmHMACSHAAuthProtocol,
    "hmac128_sha224": usmHMAC128SHA224AuthProtocol,
    "hmac192_sha256": usmHMAC192SHA256AuthProtocol,
    "hmac256_sha384": usmHMAC256SHA384AuthProtocol,
    "hmac384_sha512": usmHMAC384SHA512AuthProtocol,
    "none": usmNoAuthProtocol
}

PRIV_PROTO_MAP = {
    "des": usmDESPrivProtocol,
    "3des": usm3DESEDEPrivProtocol,
    "aes_128": usmAesCfb128Protocol,
    "aes_192": usmAesCfb192Protocol,
    "aes_256": usmAesCfb256Protocol,
    "none": usmNoPrivProtocol
}

SECURITY_LEVEL_MAPPING = {
    'noAuthNoPriv': 1,
    'authNoPriv': 2,
    'authPriv': 3,
    'no_auth_or_privacy': 1,
    'auth_without_privacy': 2,
    'auth_with_privacy': 3
}

# --- SSH Constants ---
DEV_TYPES = list(CLASS_MAPPER_BASE.keys())

MIB_MAP = {
    "sysDescr": "1.3.6.1.2.1.1.1.0",
    "sysName": ['SNMPv2-MIB', 'sysName', 0],
    "TEST": "1.3.6.1.4.1.9.9.23.1.2.1.1.8.10124.17"
}
