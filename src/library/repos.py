import logging

import requests
from sqlalchemy import text

from src.library.interface_repository import IRepository


class QueryException(Exception):

    def __init__(self):
        Exception.__init__(self)
        self.message = "Error while executing query!"


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, database_connection):
        self.database_connection = database_connection

    def _update(self, table, new_values, condition):
        self.logger.info("Updating row")
        status_code = self._send_old_row_to_coordinator(table, new_values[1])
        self.logger.info("Old row send to Coordinator with result: %s", status_code)
        stmt = text("UPDATE :table SET :values WHERE :where")
        stmt = stmt.bindparams(table=table, values=new_values[0], where=new_values[1])
        return self.database_connection.execute(stmt)

    def _insert(self, table, values):
        self.logger.info("Inserting row")
        stmt = text("INSERT INTO :table VALUES (:values)")
        stmt = stmt.bindparams(table=table, values=values)
        return self.database_connection.execute(stmt)

    def _delete(self, table, condition):
        self.logger.info("Deleting row")
        status_code = self._send_old_row_to_coordinator(table, condition)
        self.logger.info("Old row send to Coordinator with result: %s", status_code)
        stmt = text("DELETE FROM :table WHERE :where")
        stmt = stmt.bindparams(table=table, where=condition)
        return self.database_connection.execute(stmt)

    def execute_statement(self, statement):
        try:
            if statement.method == "INSERT":
                table, values = statement.toSQL()
                self._insert(table, values)
            elif statement.method == "DELETE":
                table, condition = statement.toSQL()
                self._delete(table, condition)
            else:
                table, values, condition = statement.toSQL()
                self._update(table, values, condition)
        except:
            raise QueryException

    def rollback(self):
        self.logger.warning("Performing transaction rollback")
        return self.database_connection.execute(text("ROLLBACK"))

    def commit(self):
        self.logger.info("Performing transaction commit")
        return self.database_connection.execute(text("COMMIT"))

    def begin_transaction(self):
        self.logger.info("Starting transaction")
        return self.database_connection.execute(text("BEGIN"))

    def _send_old_row_to_coordinator(self, table, conditions):
        stmt = text("SELECT * FROM :table WHERE :where")
        stmt = stmt.bindparams(table=table, where=conditions)
        old_row = self.database_connection.execute(stmt)
        # TODO: Change to cooridnator endpoint and parse select statement
        res = requests.post('http://localhost:5000/tests/endpoint', json=old_row)
        return res.status_code
