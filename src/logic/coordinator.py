import logging
import uuid as uuid
from dataclasses import dataclass

import requests

from src.entity.request import DP_Repository
from src.library.repos import QueryException
from src.logic.interface_unit_of_work import IUnitOfWork


@dataclass
class WebService:
    _url: str
    _send_transaction_endpoint: str
    _commit_endpoint: str
    _rollback_endpoint: str

    def send_transaction(self, transaction):
        return requests.post(self._url + self._send_transaction_endpoint, json=transaction)

    def commit(self):
        return requests.post(self._url + self._commit_endpoint)

    def rollback(self):
        return requests.post(self._url + self._rollback_endpoint)


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.webservices_dict = dict()  # DP_Repository
        self._committed_repository_id_list = []
        self._changed_repository_id_list = []
        self._transaction_list = []
        self._send_transactions_dict = dict()
        self._old_data_dict = {}

    def get_all_repositories(self):
        return self.webservices_dict

    def add_repository(self, webservice_data: DP_Repository):
        webservice_id = str(uuid.uuid1())
        url = "http:/" + webservice_data.host + ":" + webservice_data.port
        send_transaction_endpoint = webservice_data.endpoints[0]
        commit_endpoint = webservice_data.endpoints[1]
        rollback_endpoint = webservice_data.endpoints[2]

        self.webservices_dict[webservice_id] = WebService(url, send_transaction_endpoint, commit_endpoint,
                                                          rollback_endpoint)
        return webservice_id

    def delete_repository(self, repo_uuid):
        self.logger.info("Removing repository %s from repository dict", repo_uuid)
        try:
            return self.webservices_dict.pop(repo_uuid, None)
        except KeyError:
            self.logger.warning("Repository %s not found", repo_uuid)
            return None

    def get_repository(self, repo_uuid):
        self.logger.info("Get repository %s from repository dict", repo_uuid)
        try:
            return self.webservices_dict.get(repo_uuid, None)
        except KeyError:
            self.logger.warning("Repository %s not found", repo_uuid)
            return None

    def set_transactions(self, transactions):
        self._transaction_list = transactions

    def execute_transaction(self):
        for transaction in self._transaction_list:
            try:
                webservice = self.webservices_dict[transaction.repository_id]
                self._changed_repository_id_list.append(transaction.repository_id)
                self._send_transactions_dict[transaction.repository_id] = transaction.statments
                for statement in transaction.statments:
                    result = webservice.send_transaction(statement)
            except (KeyError, QueryException) as ex:
                self.logger.error("Repository %s not found!", transaction.repository_id)
                self.logger.exception(ex.message)
                self._rollback()

    def commit(self):
        self.logger.info("Committing changes")
        for repo_id in self._changed_repository_id_list:
            try:
                webservice = self.webservices_dict[repo_id]
                webservice.commit()
                self._committed_repository_id_list.append(repo_id)
                self._changed_repository_id_list.remove(repo_id)
            except:
                self.logger.error("Transaction failed!")
                self._rollback()
                break

        self._committed_repository_id_list.clear()
        self._changed_repository_id_list.clear()
        self._transaction_list.clear()
        self._send_transactions_dict.clear()

    def _rollback(self):
        self.logger.warning("Rolling back changes")
        for repo_id in self._changed_repository_id_list:
            webservice = self.webservices_dict[repo_id]
            webservice.rollback()
            self._send_transactions_dict.pop(repo_id)

        for repo_id in self._committed_repository_id_list:
            transactions = self._send_transactions_dict[repo_id]
            self._reverse_transactions(transactions)
            webservice = self.webservices_dict[repo_id]

            for transaction in transactions:
                webservice.send_transaction(transaction)
            webservice.commit()
        self._committed_repository_id_list.clear()
        self._changed_repository_id_list.clear()
        self._transaction_list.clear()
        self._send_transactions_dict.clear()

    @staticmethod
    def _reverse_transactions(transactions):
        for transaction in transactions:
            if transaction.method == "INSERT":
                transaction.method = "DELETE"
            elif transaction.method == "DELETE":
                transaction.method = "INSERT"
                # TODO: Change date for old ones based on self._old_data_list = []
            else:
                # TODO: Change date for update to old ones based on self._old_data_list = []
                pass
