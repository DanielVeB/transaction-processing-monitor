from src.repository.interface_repository import IRepository
import logging


class DataBaseRepository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, data_base_session):
        self.data_base_session = data_base_session

    def get(self, item):
        self.logger.info("Getting %s from Data Base", item)
        pass

    def create(self, item):
        self.logger.info("Creating %s in Data Base", item)
        pass

    def delete(self, item):
        self.logger.info("Deleting %s from Data Base", item)
        pass

    def get_all(self):
        self.logger.info("Getting all data Data Base")
        pass


class ApplicationServerRepository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, app_server_session):
        self.app_server_session = app_server_session

    def get(self, item):
        self.logger.info("Getting %s from Application Server", item)
        pass

    def create(self, item):
        self.logger.info("Creating %s in Application Server", item)
        pass

    def delete(self, item):
        self.logger.info("Deleting %s from Application Server", item)
        pass

    def get_all(self):
        self.logger.info("Getting all data form Application Server")
        pass
