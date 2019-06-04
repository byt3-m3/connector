import os

APP_PORT = os.getenv("APP_PORT", "5001")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_HOST", "27017")
DB_USER = os.getenv("DB_USER", "app")
DB_PASSWORD = os.getenv("DB_USER", "connectorapi")
APP_DB = os.getenv("APP_DB", "connector")
DEBUG = os.getenv("DEBUG", True)