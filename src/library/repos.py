from sqlalchemy import text
from src.library.interface_repository import IRepository
import logging
import requests


class Repository(IRepository):

    logger = logging.getLogger(__name__)

    def __init__(self, database_connection):
        self.database_connection = database_connection

    def update(self, table, new_values):
        self.logger.info("Updating row")
        status_code = self._send_old_row_to_coordinator(table, new_values[1])
        self.logger.info("Old row send to Coordinator with result: %s", status_code)
        stmt = text("UPDATE :table SET :values WHERE :where")
        stmt = stmt.bindparams(table=table, values=new_values[0], where=new_values[1])
        return self.database_connection.execute(stmt)

    def insert(self, table, values):
        self.logger.info("Inserting row")
        stmt = text("INSERT INTO :table VALUES (:values)")
        stmt = stmt.bindparams(table=table, values=values)
        return self.database_connection.execute(stmt)

    def delete(self, table, conditions):
        self.logger.info("Deleting row")
        status_code = self._send_old_row_to_coordinator(table, conditions)
        self.logger.info("Old row send to Coordinator with result: %s", status_code)
        stmt = text("DELETE FROM :table WHERE :where")
        stmt = stmt.bindparams(table=table, where=conditions)
        return self.database_connection.execute(stmt)

    def rollback(self):
        self.logger.info("Performing rollback")
        return self.database_connection.execute("ROLLBACK")

    def commit(self):
        self.logger.info("Performing commit")
        return self.database_connection.execute("COMMIT")

    def _send_old_row_to_coordinator(self, table, conditions):
        stmt = text("SELECT * FROM :table WHERE :where")
        stmt = stmt.bindparams(table=table, where=conditions)
        old_row = self.database_connection.execute(stmt)
        # TODO: Change to cooridnator endpoint
        res = requests.post('http://localhost:5000/tests/endpoint', json=old_row)
        return res.status_code





