from uuid import uuid1


class DpResource:

    def __init__(self, host, port, user, password):
        self.id = uuid1()
        self.host = host
        self.port = port
        self.user = user
        self.password = password

