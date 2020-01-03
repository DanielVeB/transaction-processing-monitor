from uuid import uuid1


class DpResource(object):

    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def serialize(self):
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password
        }
