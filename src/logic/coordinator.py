import uuid as uuid
from dataclasses import dataclass

import requests
from flask import jsonify

from src.entity.request import DP_Repository
from src.logic.interface_unit_of_work import IUnitOfWork


class QueryException(Exception):
    def __init__(self):
        Exception.__init__(self)


class CommitException(Exception):
    def __init__(self):
        Exception.__init__(self)


class Coordinator(IUnitOfWork):
    @dataclass
    class _WebService:
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

    def __init__(self, app):
        self.webservices_dict = dict()
        self._committed_repository_id_list = []
        self._changed_repository_id_list = []
        self._transaction_list = []
        self._send_transactions_dict = dict()
        self._reverse_transaction_dict = {}
        self.app = app

    def get_all_repositories(self):
        return self.webservices_dict

    def add_repository(self, webservice_data: DP_Repository, webservice_id=None):
        if webservice_id is None:
            webservice_id = str(uuid.uuid1())
        url = "http://" + webservice_data.host + ":" + webservice_data.port
        send_transaction_endpoint = webservice_data.endpoints[0]
        commit_endpoint = webservice_data.endpoints[1]
        rollback_endpoint = webservice_data.endpoints[2]

        self.webservices_dict[webservice_id] = self._WebService(url, send_transaction_endpoint, commit_endpoint,
                                                                rollback_endpoint)
        return webservice_id

    def delete_repository(self, repo_uuid):
        self.app.logger.info("Removing repository %s from repository dict", repo_uuid)
        try:
            return self.webservices_dict.pop(repo_uuid, None)
        except KeyError:
            self.app.logger.warning("Repository %s not found", repo_uuid)
            return None

    def get_repository(self, repo_uuid):
        self.app.logger.info("Get repository %s from repository dict", repo_uuid)
        try:
            return self.webservices_dict.get(repo_uuid, None)
        except KeyError:
            self.app.logger.warning("Repository %s not found", repo_uuid)
            return None

    def set_transactions(self, transactions):
        self._transaction_list = transactions.copy()

    def get_transaction(self):
        return self._transaction_list

    def execute_transaction(self):
        if len(self._transaction_list) == 0:
            return "There's no transaction. Please add transaction before"
        for transaction in self._transaction_list:
            try:
                self.app.logger.info(self.webservices_dict)
                webservice = self.webservices_dict[transaction.repository_id]
                self._changed_repository_id_list.append(transaction.repository_id)
                self._send_transactions_dict[transaction.repository_id] = transaction.statements
                result = webservice.send_transaction(transaction.serialize())
                self.app.logger.info("Sending request")
                if result.status_code != 200:
                    raise QueryException
                else:
                    self._reverse_transaction_dict[transaction.repository_id] = result.json()
            except (KeyError, QueryException) as ex:
                self.app.logger.error("Error executing query!")
                self._rollback()
                return "Transaction failed."
        return "Transaction executed successfully"

    def commit(self):
        self.app.logger.info("Committing changes")
        for repo_id in self._changed_repository_id_list:
            try:
                webservice = self.webservices_dict[repo_id]
                result = webservice.commit()
                if result.status_code != 200:
                    raise CommitException
                self._committed_repository_id_list.append(repo_id)
                self._changed_repository_id_list.remove(repo_id)
            except CommitException:
                self.app.logger.error("Commit failed!")
                self._rollback()
                return jsonify(error="Commit error!")

        self._committed_repository_id_list.clear()
        self._changed_repository_id_list.clear()
        self._transaction_list.clear()
        self._send_transactions_dict.clear()
        return jsonify(status="Success")

    def _rollback(self):
        self.app.logger.warning("Rolling back changes")
        for repo_id in self._changed_repository_id_list:
            webservice = self.webservices_dict[repo_id]
            webservice.rollback()

        for repo_id in self._committed_repository_id_list:
            transactions = self._reverse_transaction_dict[repo_id]
            webservice = self.webservices_dict[repo_id]

            for transaction in transactions:
                webservice.send_transaction(transaction.serialize())
            webservice.commit()

        self._committed_repository_id_list.clear()
        self._changed_repository_id_list.clear()
        self._transaction_list.clear()
        self._send_transactions_dict.clear()
