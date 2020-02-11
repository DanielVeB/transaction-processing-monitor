from dataclasses import dataclass

import requests

from src.library.execptions import MissingParametersException
from src.logic.request import Query


@dataclass
class WebServiceBuilder:
    _host: str = None
    _port: str = None
    _send_transaction_endpoint: str = "/execute"
    _commit_endpoint: str = "/commit"
    _rollback_endpoint: str = "/rollback"

    def with_host(self, host):
        self._host = host
        return self

    def with_port(self, port):
        self._port = port
        return self

    def with_send_transaction_endpoint(self, send_transaction_endpoint):
        self._send_transaction_endpoint = send_transaction_endpoint
        return self

    def with_commit_endpoint(self, commit_endpoint):
        self._commit_endpoint = commit_endpoint
        return self

    def rollback_endpoint(self, rollback_endpoint):
        self._rollback_endpoint = rollback_endpoint
        return self

    def build(self):
        if vars(self).values() is None:
            raise MissingParametersException
        url = "http://" + self._host + ":" + self._port
        return _WebService(url, self._send_transaction_endpoint, self._commit_endpoint, self._rollback_endpoint, [])


@dataclass
class _WebService:
    url: str
    _send_transaction_endpoint: str
    _commit_endpoint: str
    _rollback_endpoint: str
    query_list: []

    def add_query(self, query: Query):
        self.query_list.append(query)

    def commit(self):
        return requests.post(self.url + self._commit_endpoint)

    def rollback(self):
        return requests.post(self.url + self._rollback_endpoint)

    def send_transaction(self, content):
        return requests.post(self.url + self._send_transaction_endpoint, json=content)
