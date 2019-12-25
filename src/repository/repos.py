from src.logic.commands import Command
from src.repository.interface_repository import IRepository
import logging
from src.dto.connection import db, Test


class TestRepository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, data_base_connection):
        self.data_base_connection = data_base_connection
        self.changed_items_list = []

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        self.changed_items_list.append((item.clone(), Command.UPDATE))
        return Test.query.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.changed_items_list.append((item.clone(), Command.INSERT))
        self.data_base_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.changed_items_list.append((item.clone(), Command.DELETE))
        self.data_base_connection.session.delete(item)


data_base_repository = TestRepository(db)
