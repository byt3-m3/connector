# Connector Service 
This service is designed to handle any device communication methods that need to occur with end nodes. Protocols like 
SSH, SNMPv2, and SNMPv3 is supported by this service.

To run this up, using the run shell script on a docker host. This will launch the docker-compose file needed to lauch 
this service.


SNMPv3 is supported by this API. Each version of SNMP has its own required set of fields needed for operation. Below are
are the variations of the SNMP versions. This API is built on top of the pysnmp library. 

     
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
