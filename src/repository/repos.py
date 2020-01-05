from src.repository.interface_repository import IRepository
import logging
from src.dto.connection import Connection


class TestRepository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, connection_URI):
        self.data_base_connection = Connection.create_connection(connection_URI)

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        return self.data_base_connection.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.data_base_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.data_base_connection.session.delete(item)


