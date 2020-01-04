import logging
import uuid as uuid

from flask import jsonify

from src.dto.resource import DpResource
from src.logic.commands import Command
from src.logic.interface_unit_of_work import IUnitOfWork
from src.logic.transactions import DeleteAction, InsertAction, RestoreAction
from src.repository.repos import TestRepository


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.repository_dict = dict()
        self._committed_repository_list = []
        self._changes_list = []

    def get_all_repositories(self):
        return self.repository_dict

    def add_repositories(self,repositories: [DpResource]):
        id = str(uuid.uuid1())
        for repo in repositories:
            self.repository_dict[id] = repo
        return id

    def delete_repository(self, repo_uuid):
        self.logger.info("Removing repository %s from repository list", repo_uuid)
        return self.repository_dict.pop(repo_uuid, None)

    def get_repository(self, repo_uuid):
        self.logger.info("Get repository %s from repository list", repo_uuid)
        return self.repository_dict.get(repo_uuid, None)

    # @app.route('/coordinator/commit', methods=['GET'])
    def commit(self):
        self.logger.info("Committing changes")
        for repo in self.repository_dict.values():
            try:
                repo.data_base_connection.session.commit()
                self._committed_repository_list.append(repo.data_base_connection)
            except:
                self.rollback()
        self._committed_repository_list.clear()
        self._changes_list.clear()

    def rollback(self):
        self.logger.warning("Rolling back changes")
        for repo, change in self._committed_repository_list, self._changes_list:
            if repo is change.repo:
                if change.command == Command.INSERT:
                    DeleteAction(change.item, change.repo).execute()
                elif change.command == Command.DELETE:
                    InsertAction(change.item, change.repo).execute()
                else:
                    RestoreAction(change.item, change.old_item, change.repo).execute()
            repo.data_base_connection.session.commit()

        for repo in self.repository_dict.values():
            repo.data_base_connection.session.clear()

    def add_repository(self, connection):
        repo = TestRepository(connection)
        repo_uuid = uuid.UUID
        self.logger.info("Adding repository %s to repository list", repo.__name__)
        self.repository_dict[repo_uuid] = repo
        return jsonify(repo_uuid)

    def execute_command(self, action, repo_uuid):
        if repo_uuid in self.repository_dict:
            repo = self.repository_dict.get(repo_uuid)
            self.logger.info("Executing command for %s repository", repo.__name__)
            action.execute()
            self._changes_list.append((repo_uuid, action))
        else:
            self.logger.exception("Repo %s not found in repository list", repo_uuid)
