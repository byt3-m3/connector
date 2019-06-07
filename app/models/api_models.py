from . import Schema, Optional
from app.models import request_pb2
import json


METHOD_TYPES = ['ssh_cmd']

# This Model represents a basic API request
APIRequestSchema = Schema({
    'method': str,
    "params": dict,
    Optional("opts"): dict,
    Optional("filters"): dict,
})

