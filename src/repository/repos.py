from src.repository.interface_repository import IRepository
import logging
from src.dto.connection import Connection


# Trzeba by zrobic klase osobna dla kazdego rodzaju bazy, tylko ze one sie specjalnie nie beda roznic

# TODO: To w sumie srednio pasuje i raczejbym tego nie robil fabrykowa typowo javowa
class TestMySQL(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, data_base_connection, binds):
        self.data_base_connection = Connection.create_connection(data_base_connection, binds)

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        return self.data_base_connection.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.data_base_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.data_base_connection.session.delete(item)


class TestPostGreSQL(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, data_base_connection, binds):
        self.data_base_connection = Connection.create_connection(data_base_connection, binds)

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        return self.data_base_connection.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.data_base_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.data_base_connection.session.delete(item)


class TestOracle(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, data_base_connection, binds):
        self.data_base_connection = Connection.create_connection(data_base_connection, binds)

    def get(self, item):
        self.logger.info("Getting %s from DataBase", item)
        return self.data_base_connection.filter(item).first()

    def insert(self, item):
        self.logger.info("Creating %s in DataBase", item)
        self.data_base_connection.session.add(item)

    def delete(self, item):
        self.logger.info("Deleting %s from DataBase", item)
        self.data_base_connection.session.delete(item)

# data_base_repository = TestRepository(db)
