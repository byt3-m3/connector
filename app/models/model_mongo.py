from pymongo import MongoClient

from config import DB_USER, APP_DB, DB_HOST, DB_PASSWORD, DB_PORT


class ModelMongo:

    def __init__(self, *args, **kwargs):
        # Extracts database host and port
        self._db_host = kwargs.get("db_host", DB_HOST)
        self._db_port = kwargs.get("db_port", DB_PORT)

        # checks of auth flag is set, if True, use the auth method of the Mongoclient.
        self._auth = kwargs.get("auth", True)
        if self._auth is True:
            try:
                self._mc = MongoClient(host=f'{self._db_host}:{self._db_port}', username=DB_USER, password=DB_PASSWORD,
                                       authSource=APP_DB)

            except Exception as err:
                raise (err)
        else:
            try:
                self._mc = MongoClient(host=f'{self._db_host}:{self._db_port}')
            except Exception as err:
                raise (err)

        # Extracts the Database name and attempts to make a connection to the database
        self._db_name = kwargs.get("db_name", APP_DB)
        if self._db_name:
            try:
                self.connect_db(self._db_name)

            except Exception as err:
                raise (err)
        else:
            self.db = None

        # Extracts the collection name and attempts to connect to the collection
        self.collection = kwargs.get("collection")
        if self.collection:
            self.connect_collection(self.collection)
        else:
            self.collection = None

    def set_db_host(self, hostAddr):
        self._db_host = hostAddr

    def set_db_port(self, hostPort):
        self._db_port = hostPort

    def connect_db(self, db_name):
        if self._mc:
            self.db = self._mc[db_name]
            return True

        else:
            return False

    def connect_collection(self, collection):
        if self.db:
            self.collection = self.db['collection']
