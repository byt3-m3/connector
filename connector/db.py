from pymongo import MongoClient

_DB_HOST = MongoClient("192.168.99.100:27017")
_CONNECTOR_DB = _DB_HOST['connector']


