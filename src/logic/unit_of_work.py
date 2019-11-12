from src.logic.interface_unit_of_work import IUnitOfWork
from src.repository.repos import DataBaseRepository, ApplicationServerRepository
import logging


class UnitOfWork(IUnitOfWork):
    logger = logging.getLogger(__name__)

    def __init__(self, session):
        self.session = session
        self.data_base_repository = DataBaseRepository(session)
        self.app_server_repository = ApplicationServerRepository(session)

    def register_new(self):
        self.logger.info("Registering new object")
        print("register_new")

    def register_dirty(self):
        print("register_dirty")

    def register_clean(self):
        print("register_clean")

    def register_delete(self):
        print("register_delete")

    def commit(self):
        self.logger.info("Commit all changes")
        print("commit")

    def rollback(self):
        self.logger.error("Rollback of all objects started")
        print("rollback")
