from uuid import uuid1


class DpResource(object):

    def __init__(self, type,  host, port, user, password):
        self.type = type
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def serialize(self):
        return {
            "self.type": self.type,
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password
        }
