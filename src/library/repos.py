from src.library.interface_repository import IRepository
import logging


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, database_connection):
        self.database_connection = database_connection

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        return self.database_connection.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.database_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.database_connection.session.delete(item)


