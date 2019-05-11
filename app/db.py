from pymongo import MongoClient

_DB_HOST = MongoClient("192.168.99.100:27017")
_CONNECTOR_DB = _DB_HOST['connector']
_MODEL_COLLECTION = _CONNECTOR_DB['models']
_MODELS_POINTER = _MODEL_COLLECTION.find({}, {'_id': False})


MODEL_LIST = [a for a in _MODELS_POINTER if a['type']]

