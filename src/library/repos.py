import logging

from sqlalchemy import text

from src.library.interfaces import IRepository
from src.logic.request import Query


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
        for transaction in statement["statements"]:
            try:
                if transaction.method == "INSERT":
                    sql_query, select_to_reverse = transaction.to_sql()
                    stmt = text(select_to_reverse)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_reverse_query(transaction, data_select))
                    self._insert(sql_query)
                elif transaction.method == "DELETE":
                    sql_query, select_to_reverse = transaction.to_sql()
                    stmt = text(select_to_reverse)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_reverse_query(transaction, data_select))
                    self._delete(sql_query)
                else:
                    sql_query, select_to_reverse = transaction.to_sql()
                    stmt = text(select_to_reverse)
                    data_select = self.database_connection.execute(stmt)
                    result.append(self.create_reverse_query(transaction, data_select))
                    self._update(sql_query)
            except:
                self.logger.error("Transaction failed!")
        return result

    def rollback(self):
        self.app.logger.warning("Performing transaction rollback")
        self.database_connection.rollback()

    def commit(self):
        self.app.logger.info("Performing transaction commit")
        self.database_connection.commit()

    @staticmethod
    def create_reverse_query(transaction, values=None):
        if values is None:
            values = {}
        if transaction.method == "INSERT":
            where = ""
            name_of_values = list(transaction.values.values())
            for i in range(0, len(name_of_values)):
                where += name_of_values[i] + "=" + values[0][i] + " AND "
            where = where[:-4]

            result = "DELETE FROM " + transaction.table_name + " where " + where

            return result
        elif transaction.method == "UPDATE":
            name_of_values = list(transaction.values.values())
            result = "UPDATE " + transaction.table_name + " SET "
            for i in range(0, len(name_of_values)):
                if isinstance(values[0][i], int):
                    result += name_of_values[i] + " = " + str(values[0][i]) + ","
                else:
                    result += name_of_values[i] + " = '" + values[0][i] + "',"
            result = result[:-1]

            if transaction.where is not None:
                result += " WHERE " + transaction.where

            return result
        else:
            keys = ','.join(transaction.values.keys())
            result = transaction.method + " INTO " + transaction.table_name + "(" + keys + ")" + " VALUES "
            for i in range(0, len(keys)):
                if isinstance(values[0][i], int):
                    result += str(values[0][i]) + ","
                else:
                    result += "'" + values[0][i] + "',"
            result = result[:-1]
            if transaction.where is not None:
                result += " WHERE " + transaction.where

            return result


def get_values(statement):
    try:
        values_dict = {}
        values = statement['values']
        for value in values:
            key = value['key']
            val = value['value']
            values_dict[key] = val
        return values_dict
    except:
        return {}


def get_where(statement):
    try:
        return statement['where']
    except:
        return None


class RepoCoordinator:

    def __init__(self, repository: Repository):
        self.repository = repository
        self.data_to_reverse = []

    def rollback(self):
        self.repository.rollback()

    def commit(self):
        self.repository.commit()

    def execute_transaction(self, transaction):
        statements = []
        for statement in transaction['statements']:
            statements.append(
                Query(
                    method=statement['method'],
                    table_name=statement['table_name'],
                    values=get_values(statement),
                    where=get_where(statement)
                )
            )
            statements.append(statement)
        self.data_to_reverse = self.repository.execute_statement(statements)
