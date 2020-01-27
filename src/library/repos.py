import json
import logging

from sqlalchemy import text

from src.library.interfaces import IRepository


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, database_connection, app):
        self.database_connection = database_connection
        self.app = app

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
        for transaction in statement["statements"]:
            try:
                if transaction.method == "INSERT":
                    table, select = transaction.to_sql()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_json(transaction, "INSERT", data_select))
                    self._insert(table)
                elif transaction.method == "DELETE":
                    table, select = transaction.to_sql()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_json(transaction, "DELETE", data_select))
                    self._delete(table)
                else:
                    table, values = transaction.to_sql()
                    stmt = text(select)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_json(transaction, "UPDATE", data_select))
                    self._update(table)
            except:
                self.logger.error("Transaction failed!")
        result = {"statements": result}
        return result

    def rollback(self):
        self.app.logger.warning("Performing transaction rollback")
        return self.database_connection.execute(text("ROLLBACK"))

    def commit(self):
        self.app.logger.info("Performing transaction commit")
        return self.database_connection.execute(text("COMMIT"))

    def begin_transaction(self):
        self.app.logger.info("Starting transaction")
        return self.database_connection.execute(text("BEGIN"))

    @staticmethod
    def create_json(transaction, query_type, values=None):
        if values is None:
            values = {}
        if query_type == "INSERT":
            where = ""
            name_of_values = list(transaction.values.values())
            for i in range(0, len(name_of_values)):
                where += name_of_values[i] + "=" + values[0][i] + " AND "
            where = where[:-4]
            element = {"method": "DELETE", "table_name": transaction.table_name, "where": where}
            result = json.dumps(element)
            return result
        elif query_type == "UPDATE":
            update_list = []
            name_of_values = list(transaction.values.values())
            for j in range(0, len(values)):
                val = []
                for i in range(0, len(name_of_values)):
                    val.append(name_of_values[i] + ":" + values[j][i])
                element = {"method": transaction.method, "table_name": transaction.table_name, "values": val,
                           "where": transaction.where}
                update_list.append(element)
            result = json.dumps(update_list)
            return result
        else:
            insert_list = []
            name_of_values = list(transaction.values.values())
            for j in range(0, len(values)):
                val = []
                for i in range(0, len(name_of_values)):
                    val.append(name_of_values[i] + ":" + values[j][i])
                element = {"method": "INSERT", "table_name": transaction.table_name, "values": values}
                insert_list.append(element)
            result = json.dumps(insert_list)
            return result
