from src.logic.interface_unit_of_work import IUnitOfWork
from src.library.repos import Repository, ApplicationServerRepository
import logging


class UnitOfWork(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self, session):
        self.session = session
        self.data_base_repository = Repository(session)
        self.app_server_repository = ApplicationServerRepository(session)

    def add_repository(self, repo):
        self.logger.info("Adding new repo")
        print("register_new")

    def delete_repository(self, repo):
        self.logger.info("Deleting repo")

    def commit(self):
        self.logger.info("Commit all changes")
        print("commit")

    def _rollback(self):
        self.logger.error("Rollback of all objects started")
        print("rollback")
