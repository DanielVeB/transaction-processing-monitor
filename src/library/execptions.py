class QueryException(Exception):
    def __init__(self):
        super().__init__()


class CommitException(Exception):
    def __init__(self, webservice_url):
        super().__init__()
        self.webservice_url = webservice_url


class TransactionException(Exception):
    def __init__(self, webservice_url):
        self.webservice_url = webservice_url
        self.message = "Transaction failed for: " + webservice_url
        super().__init__(self.message)
