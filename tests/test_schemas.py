import unittest
from connector.models import (
    DiscoverSNMPv3,
    DiscoverSNMPv2,
    SSHCommandSchema
)


class MyTestCase(unittest.TestCase):
    def test_schema_ssh_command(self):
        schema = SSHCommandSchema()

        data = {
            "node_type": "cisco_ios",
            "username": "cisco",
            "password": "cisco",
            "cmd": "show ip route",
            "target": "192.168.1.2",
            "ssh_priv_key": "",
            "ssh_pub_key": ""
        }

        validation_result = schema.validate(data)
        self.assertEqual(validation_result, {})

        # Tests if invalid node_type param is provided
        data = {
            "node_type": "bad_type",
            "username": "cisco",
            "password": "cisco",
            "cmd": "show ip route",
            "target": "192.168.1.2",
            "ssh_priv_key": "",
            "ssh_pub_key": ""
        }

        validation_result = schema.validate(data)
        self.assertEqual(len(validation_result), 1)

        # Tests if missing required params
        data = {
            "cmd": "show ip route",
            "ssh_priv_key": "",
            "ssh_pub_key": ""
        }
        validation_result = schema.validate(data)
        self.assertEqual(len(validation_result), 4)

        # Tests all possible timeout values
        for i in range(100):
            data = {
                "node_type": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show ip route",
                "target": "192.168.1.2",
                "timeout": i + 1,
                "ssh_pub_key": ""
            }
            validation_result = schema.validate(data)
            self.assertEqual(validation_result, {})

            # Tests max timeout value
            data = {
                "node_type": "cisco_ios",
                "username": "cisco",
                "password": "cisco",
                "cmd": "show ip route",
                "target": "192.168.1.2",
                "timeout": 101,
                "ssh_pub_key": ""
            }
            validation_result = schema.validate(data)
            self.assertEqual(len(validation_result), 1)


if __name__ == '__main__':
    unittest.main()
