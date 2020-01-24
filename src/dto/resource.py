from uuid import uuid1
from src.library.repos import Repository
from src.library.connection_config import URI


class DpResource(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serialize(self):
        return {
            "host": self.host,
            "port": self.port,
        }
