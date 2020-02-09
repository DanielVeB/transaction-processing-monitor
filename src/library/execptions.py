class QueryException(Exception):
    def __init__(self):
        super().__init__()


class CommitException(Exception):
    def __init__(self, webservice_url):
        super().__init__()
        self.webservice_url = webservice_url


class TransactionException(Exception):
    def __init__(self):
        self.message = "Transaction failed!"
        super().__init__(self.message)


class MissingParametersException(Exception):
    def __init__(self):
        self.message = "Not all required parameters were given!"
        super().__init__(self.message)
