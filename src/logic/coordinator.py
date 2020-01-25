import logging
import uuid
from dataclasses import dataclass

import requests

from src.entity.request import WebServiceData
from src.logic.interface_unit_of_work import IUnitOfWork


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


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    @dataclass
    class _WebService:
        url: str
        _send_transaction_endpoint: str
        _commit_endpoint: str
        _rollback_endpoint: str
        query_list: [] = None

        def add(self, table, values):
            pass

        def remove(self, table, where):
            pass

        def update(self, table, values, where):
            pass

        def commit(self):
            return requests.post(self.url + self._commit_endpoint)

        def rollback(self):
            return requests.post(self.url + self._rollback_endpoint)

    def __init__(self):
        self._webservices_dict = dict()
        self._committed_webservice_uuid_list = list()
        self._changed_webservice_uuid_list = list()
        self._send_queries_dict = dict()
        self._reverse_transaction_dict = dict()

    def get_all_services(self):
        self.logger.info("Getting services url list")
        webservices_url_list = []
        for service in self._webservices_dict.values():
            webservices_url_list.append(service.url)
        return webservices_url_list

    def add_service(self, webservice_data: WebServiceData):
        webservice_id = uuid.uuid4()
        url = "http://" + webservice_data.host + ":" + webservice_data.port
        send_transaction_endpoint = webservice_data.endpoints[0]
        commit_endpoint = webservice_data.endpoints[1]
        rollback_endpoint = webservice_data.endpoints[2]

        webservice = self._WebService(url, send_transaction_endpoint, commit_endpoint,
                                      rollback_endpoint)

        self._webservices_dict[webservice_id] = webservice
        return webservice

    def delete_service(self, webservice: _WebService):
        self.logger.info("Removing service %s from Coordinator", webservice.url)
        for key, value in self._webservices_dict:
            if value == webservice:
                self._webservices_dict.pop(key)
                return

        self.logger.warning("Service %s not found!", webservice.url)

    def execute_transaction(self):
        if len(self._webservices_dict) == 0:
            self.logger.error("No services found!")
            return

        for key, webservice in self._webservices_dict:
            try:
                self.logger.info("Sending queries to %s", webservice.url)
                self._changed_webservice_uuid_list.append(key)
                self._send_queries_dict[key] = webservice.query_list
                result = webservice.send_transaction(webservice.query_list.serialize())
                self.logger.info("Sending request")
                if result.status_code != requests.codes.ok:
                    raise QueryException()
                else:
                    self._reverse_transaction_dict[key] = result.json()
            except (KeyError, QueryException):
                self.logger.error("Error while executing query for %s", webservice.url)
                self._rollback()
                raise TransactionException(webservice_url=webservice.url)

    def commit(self):
        self.logger.info("Committing changes")
        for webservice_uuid in self._changed_webservice_uuid_list:
            try:
                webservice = self._webservices_dict[webservice_uuid]
                result = webservice.commit()
                if result.status_code != requests.codes.ok:
                    raise CommitException(webservice_url=webservice.url)
                else:
                    self._committed_webservice_uuid_list.append(webservice_uuid)
                    self._changed_webservice_uuid_list.remove(webservice_uuid)
                    self.logger.info("Added %s to committed webservices list", webservice.url)
            except CommitException as ex:
                self.logger.error("Commit failed for %s", ex.webservice_url)
                self._rollback()
                raise TransactionException(webservice_url=ex.webservice_url)

        self.logger.info("Commit successful!")
        self.logger.info("Clearing query data")
        self._committed_webservice_uuid_list.clear()
        self._changed_webservice_uuid_list.clear()
        self._send_queries_dict.clear()

    def _rollback(self):
        self.logger.warning("Rolling back changes!")
        for webservice_uuid in self._changed_webservice_uuid_list:
            webservice = self._webservices_dict[webservice_uuid]
            webservice.rollback()
            self.logger.info("Rolled back transaction for %s", webservice.url)

        for webservice_uuid in self._committed_webservice_uuid_list:
            transactions = self._reverse_transaction_dict[webservice_uuid]
            webservice = self._webservices_dict[webservice_uuid]

            for transaction in transactions:
                self.logger.info("Rolling back committed changes for %s", webservice.url)
                webservice.send_transaction(transaction.serialize())

            self.logger.info("Committing rolled back changes for %s", webservice.url)
            webservice.commit()

        self.logger.info("Rollback successful!")
        self.logger.info("Clearing query data")
        self._committed_webservice_uuid_list.clear()
        self._changed_webservice_uuid_list.clear()
        self._send_queries_dict.clear()
