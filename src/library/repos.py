import json
import logging

from sqlalchemy import text
from src.library.main import app

from src.library.interface_repository import IRepository


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, database_connection):
        self.database_connection = database_connection

    def _update(self, request):
        self.logger.info("Updating row")
        stmt = text(request)
        return self.database_connection.execute(stmt)

    def _insert(self, request):
        self.logger.info("Inserting row")
        stmt = text(request)
        return self.database_connection.execute(stmt)

    def _delete(self, request):
        self.logger.info("Deleting row")
        stmt = text(request)
        return self.database_connection.execute(stmt)

    def execute_statement(self, statement):
        result = []
        self.begin_transaction()
        for transaction in statement.statements():
            try:
                if transaction.method == "INSERT":
                    table, values = transaction.toSQL()
                    self._insert(table)
                elif transaction.method == "DELETE":
                    table, values = transaction.toSQL()
                    self._delete(table)
                    result.append(self.createJSON(transaction))
                else:
                    table, values = transaction.toSQL()
                    self._update(table)
                    result.append(self.createJSON(transaction, values))
            except:
                print("Error: transaction failed")
        result = {"statements": result}
        return result

    def rollback(self):
        app.logger.warning("Performing transaction rollback")
        return self.database_connection.execute(text("ROLLBACK"))

    def commit(self):
        app.logger.info("Performing transaction commit")
        return self.database_connection.execute(text("COMMIT"))

    def begin_transaction(self):
        app.logger.info("Starting transaction")
        return self.database_connection.execute(text("BEGIN"))

    def createJSON(self, transaction, type, values={}):
        if type == "INSERT":
            where = ""
            name_of_values = list(transaction.values.values())
            for i in range(0, len(name_of_values)):
                where += name_of_values[i] + "=" + values[0][i] + " AND "
            where = where[:-4]
            element = {"method": "DELETE", "table_name": transaction.table_name, "where": where}
            result = json.dump(element)
            return result
        elif type == "UPDATE":
            val = []
            name_of_values = list(transaction.values.values())
            for i in range(0, len(name_of_values)):
                val.append(name_of_values[i] + ":" + values[i])
            element = {"method": transaction.method, "table_name": transaction.table_name, "values": val,
                       "where": transaction.where}
            result = json.dump(element)
            return result
        else:
            element = {"method": transaction.method, "table_name": transaction.table_name, "values": values,
                       "where": transaction.where}
            result = json.dump(element)
            return result
