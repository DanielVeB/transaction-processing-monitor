import logging

from src.logic.interface_unit_of_work import IUnitOfWork


class Coordinator(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.repository_list = []
        self._committed_repository_list = []
        self._changes_list = []

    def delete_repository(self, repo):
        self.logger.info("Removing repository %s from repository list", repo.__name__)
        self.repository_list.remove(repo)

    def commit(self):
        self.logger.info("Committing changes")
        for repo in self.repository_list:
            try:
                repo.data_base_connection.session.commit()
                self._committed_repository_list.append(repo.data_base_connection)
            except:
                self.rollback()

    def rollback(self):
        self.logger.warning("Rolling back changes")
        for repo in self._committed_repository_list:
            for change in self._changes_list:
                repo_change, executed_command = change
                if repo_change is repo:
                    repo.reverse_command(executed_command)
            repo.data_base_connection.session.commit()

        for repo in self.repository_list:
            repo.data_base_connection.session.clear()

    def add_repository(self, repo):
        self.logger.info("Adding repository %s to repository list", repo.__name__)
        self.repository_list.append(repo)

    def execute_command(self, command, repo):
        if repo in self.repository_list:
            self.logger.info("Executing command for %s repository", repo.__name__)
            repo.execute_command(command)
            self._changes_list.append((repo, command))
        else:
            self.logger.exception("Repo %s not found in repository list", repo.__name__)