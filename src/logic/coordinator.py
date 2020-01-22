import logging
import uuid as uuid

from src.dto.resource import DpResource
from src.logic.interface_unit_of_work import IUnitOfWork
from src.logic.commands import Command

class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.repository_dict = dict()
        self._committed_repository_list = []
        self._changed_repository_list = []
        self._transaction_list = []

    def get_all_repositories(self):
        return self.repository_dict

    def add_repository(self, repositories: [DpResource]):
        id = str(uuid.uuid1())
        for repo in repositories:
            self.repository_dict[id] = repo
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
        for repo in self.repository_dict.values():
            try:
                repo.data_base_connection.session.commit()
                self._committed_repository_list.append(repo.data_base_connection)
            except:
                self._rollback()
        self._committed_repository_list.clear()

    def _rollback(self):
        self.logger.warning("Rolling back changes")
        for repo in self._changed_repository_list:
            repo.rollback()

        for repo in self._committed_repository_list:
            # TODO: revert transaction
            pass

    def execute_transaction(self):
        for transaction in self._transaction_list:
            try:
                repository = self.repository_dict[transaction.id]
                repository.begin_transaction()
                if transaction.statment[0] == Command.INSERT:
                    repository.insert(transaction.table, transaction.statment[1])
                elif transaction.statment[0] == Command.DELETE:
                    repository.delete(transaction.table, transaction.statment[1])
                else:
                    repository.update(transaction.table, transaction.statment)
                self._changed_repository_list.append(repository)
            except KeyError:
                self.logger.error("Repository %s not found!", transaction.id)
                self._rollback()
