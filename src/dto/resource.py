from uuid import uuid1


class DpResource(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def serialize(self):
        return {
            "host": self.host,
            "port": self.port,
        }
