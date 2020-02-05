import json
import logging
import uuid

import requests

from src.library.execptions import QueryException, TransactionException, CommitException
from src.library.interfaces import IUnitOfWork
from src.logic.request import QueryEncoder


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

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

    def add_service(self, webservice):
        webservice_id = str(uuid.uuid4())
        self._webservices_dict[webservice_id] = webservice

    def delete_service(self, webservice):
        self.logger.info("Removing service %s from Coordinator", webservice.url)
        for key, value in self._webservices_dict:
            if value == webservice:
                self._webservices_dict.pop(key)
                self.logger.info("Service %s from Coordinator", webservice.url)
                return

        self.logger.warning("Service %s not found!", webservice.url)

    def execute_transaction(self):
        if len(self._webservices_dict) == 0:
            self.logger.error("No services found!")
            return

        for key, webservice in self._webservices_dict.items():
            try:
                self.logger.info("Sending queries to %s", webservice.url)
                self._changed_webservice_uuid_list.append(key)
                self._send_queries_dict[key] = webservice.query_list
                dict_to_send = dict()
                dict_to_send['statements'] = json.dumps(webservice.query_list, cls=QueryEncoder)
                result = webservice.send_transaction(dict_to_send)
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
        webservices_to_be_committed = self._changed_webservice_uuid_list.copy()
        for webservice_uuid in webservices_to_be_committed:
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
            dict_to_send = dict()
            dict_to_send['reverse'] = transactions
            self.logger.info("Rolling back committed changes for %s", webservice.url)

            webservice.send_transaction(dict_to_send)
            self.logger.info("Committing rolled back changes for %s", webservice.url)

        self.logger.info("Rollback successful!")
        self.logger.info("Clearing query data")
        self._committed_webservice_uuid_list.clear()
        self._changed_webservice_uuid_list.clear()
        self._send_queries_dict.clear()
