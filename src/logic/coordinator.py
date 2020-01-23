import logging
import uuid as uuid

from src.dto.resource import DpResource
from src.library.repos import QueryException
from src.logic.interface_unit_of_work import IUnitOfWork


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.repository_dict = dict()
        self._committed_repository_id_list = []
        self._changed_repository_id_list = []
        self._transaction_list = []
        self._send_transactions_dict = dict()
        self._old_data_list = []

    def get_all_repositories(self):
        return self.repository_dict

    def add_repository(self, repositories: [DpResource]):
        id = str(uuid.uuid1())
        for repo in repositories:
            self.repository_dict[id] = repo
            repo.connect_to_db()
        return id

    def delete_repository(self, repo_uuid):
        self.logger.info("Removing repository %s from repository dict", repo_uuid)
        try:
            return self.repository_dict.pop(repo_uuid, None)
        except KeyError:
            self.logger.warning("Repository %s not found", repo_uuid)
            return None

    def get_repository(self, repo_uuid):
        self.logger.info("Get repository %s from repository dict", repo_uuid)
        try:
            return self.repository_dict.get(repo_uuid, None)
        except KeyError:
            self.logger.warning("Repository %s not found", repo_uuid)
            return None

    def commit(self):
        self.logger.info("Committing changes")
        for repo_id in self._changed_repository_id_list:
            try:
                self.repository_dict[repo_id].commit()
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
        for repo in self._changed_repository_id_list:
            repo.rollback()
            self._send_transactions_dict.pop(repo)

        for repo_id in self._committed_repository_id_list:
            committed_repository = self.repository_dict[repo_id]
            transactions = self._send_transactions_dict[repo_id]
            self._reverse_transactions(transactions)
            for transaction in transactions:
                committed_repository.execute_statement(transaction)
            committed_repository.commit()

        self._committed_repository_id_list.clear()
        self._changed_repository_id_list.clear()
        self._transaction_list.clear()
        self._send_transactions_dict.clear()

    def set_transactions(self, transactions):
        self._transaction_list = transactions

    def execute_transaction(self):
        for transaction in self._transaction_list:
            try:
                repository = self.repository_dict[transaction.id]
                repository.begin_transaction()
                self._changed_repository_id_list.append(transaction.id)
                self._send_transactions_dict[transaction.id] = transaction.statments
                for statement in transaction.statments:
                    repository.execute_statement(statement)
            except (KeyError, QueryException) as ex:
                self.logger.error("Repository %s not found!", transaction.id)
                self.logger.exception(ex.message)
                self._rollback()

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
