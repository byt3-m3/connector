# Connector Service 
This service is designed to handle any device communication methods that need to occur with end nodes. Protocols like 
SSH, SNMPv2, and SNMPv3 is supported by this service.

To run 
```bash
python run.py 
```

## Model Info:
To use this API the following JSON body must be supplied 
```json
{
 
    "method" : "",
    "params" : "",
    "opts" : "",
    "filters" : ""
  
}
```

SNMPv3 is supported by this API. Each version of SNMP has its own required set of fields needed for operation. Below are
are the variations of the SNMP versions. This API is built on top of the pysnmp library. 

  
- SNMPv2 params:
    ```json
    {
        "community" : "",
        "target" : "",
        "version" : 2,
        "opts" : {}  
    }        
    ```

- SNMPv3 params:
    ```json
    {
        "v3_auth_key" : "",
        "v3_priv_key" : "",
        "v3_user" : "",
        "v3_usm" : "",
        "v3_auth_proto" : "",
        "v3_priv_proto" : "",
        "target" : "",
        "version" : 3,
        "opts" : {}  
    }        
    ```
    
- Supported v3 Authentication Protocols
     - "hmac_md5"
     - "hmac_sha"
     -  "hmac128_sha224"
     -  "hmac192_sha256"
     -  "hmac256_sha384"
     -  "hmac384_sha512"
     -  "none"
     
- Supported v3 Privacy Protocols
    - "des"
    - "3des"
    - "aes_128"
    - "aes_192"
    - "aes_256"
    - "none"

#### JSON Fields:
 - method: Determines which protocol will be used for the connection 
 - params: Required parameters needed to utilize the method 
 - opts: Optional features that can be used to enhance the API capability 
 - filters: Filters used for manipulating API responses
 
 ## EndPoints 
 
 ### /api/v1/access
 This endpoint is used to preform SSH or SNMP based commands
 - Methods
    - ssh_cmd 
        - params: 
            ```json
            {
                "node_type" : "",
                "ssh_username" : "",
                "ssh_password" : "",
                "cmd" : "",
                "target" : "",
                "ssh_private_key" : "",
                "ssh_public_key" : "",
                "opts" : {}
            }
            ```
    - snmp_hostname
        - params: Uses the variations of SNMP parameters as mentioned above.
    - snmp_devtype:
        - params: Uses the variations of SNMP parameters as mentioned above. 
    
# Examples
This is an SSH command request to the /api/v1/access endpoint to send a command to a  Cisco device.
```json
{
    "method": "ssh_cmd",
    "params": {
        "node_type": "cisco_ios",
        "ssh_username": "cisco",
        "ssh_password": "cisco",
        "cmd": "show ip route",
        "target": "192.168.1.2",
        "ssh_private_key": "",
        "ssh_public_key": ""
    },
    "opts": {
        "response_type": "list"
    },
    "filters": {}
}
```

Response:
```json
{
    "response": [
        "Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP",
        "       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area ",
        "       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2",
        "       E1 - OSPF external type 1, E2 - OSPF external type 2",
        "       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2",
        "       ia - IS-IS inter area, * - candidate default, U - per-user static route",
        "       o - ODR, P - periodic downloaded static route",
        "",
        "Gateway of last resort is 192.168.1.1 to network 0.0.0.0",
        "",
        "C    192.168.1.0/24 is directly connected, Vlan99",
        "S*   0.0.0.0/0 [1/0] via 192.168.1.1"
    ],
    "msg": null,
    "exception": null
}

```


This is an SNMPv3 authpriv  method to the /api/v1/access endpoint. The authentication protocol is SHA and the privacy
protocol is AES256
```json
{
    "method": "snmp_hostname",
    "params": {
        "v3_user": "usm_auth_priv",
        "v3_auth_key": "cisco1234",
        "v3_priv_key": "cisco1234",
        "v3_auth_proto": "hmac_sha",
        "v3_priv_proto": "aes_256",
        "v3_usm": "authpriv",
        "target": "192.168.1.250",
        "version": 3
    },
    "opts": {},
    "filters": {}
}
```

Response:
```json
{
    "response": {
        "hostname": "CORE-SW"
    },
    "msg": null,
    "exception": null
}
```