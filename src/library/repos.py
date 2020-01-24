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
                    table, select = transaction.toSQL()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.createJSON(transaction, "INSERT", data_select))
                    self._insert(table)
                elif transaction.method == "DELETE":
                    table, select = transaction.toSQL()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.createJSON(transaction, "DELETE", data_select))
                    self._delete(table)
                else:
                    table, values = transaction.toSQL()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.createJSON(transaction, "UPDATE", data_select))
                    self._update(table)
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
            result = json.dumps(element)
            return result
        elif type == "UPDATE":
            updateLst = []
            name_of_values = list(transaction.values.values())
            for j in range(0, len(values)):
                val = []
                for i in range(0, len(name_of_values)):
                    val.append(name_of_values[i] + ":" + values[j][i])
                element = {"method": transaction.method, "table_name": transaction.table_name, "values": val,
                           "where": transaction.where}
                updateLst.append(element)
            result = json.dumps(updateLst)
            return result
        else:
            insertLst = []
            name_of_values = list(transaction.values.values())
            for j in range(0, len(values)):
                val = []
                for i in range(0, len(name_of_values)):
                    val.append(name_of_values[i] + ":" + values[j][i])
                element = {"method": "INSERT", "table_name": transaction.table_name, "values": values}
                insertLst.append(element)
            result = json.dumps(insertLst)
            return result
