from uuid import uuid1
from src.library.repos import Repository
from src.library.connection_config import URI
from src.library.repo_factory import RepoFactory


class DpResource(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.db = None

    def serialize(self):
        return {
            "host": self.host,
            "port": self.port,
        }

    # connection can be provided manually or just choose from 3 db types, and rest is taken from connection config
    # tbh, needs better idea
    def connect_to_db(self, connection, db_type="mysql"):
        self.db = Repository(connection) if connection is not None else RepoFactory.create_repository(db_type, URI)
