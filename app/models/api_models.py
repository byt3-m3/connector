from . import Schema, Optional

METHOD_TYPES = ['ssh_cmd']

# This Model represents a basic API request
APIRequestSchema = Schema({
    'method': str,
    "params": dict,
    Optional("opts"): dict,
    Optional("filters"): dict,
})

