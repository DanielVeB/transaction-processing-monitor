import json
import logging

from MySQLdb._exceptions import IntegrityError
from flask import jsonify
from sqlalchemy import text

from src.library.execptions import TransactionException
from src.library.interfaces import IRepository
from src.logic.request import Query


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, session, app):
        self.database_connection = session()
        self.app = app

    def _update(self, request):
        self.logger.info("Updating row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def _insert(self, request):
        self.logger.info("Inserting row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def _delete(self, request):
        self.logger.info("Deleting row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def execute_statement(self, transaction):
        result = []
        for query in transaction:
            try:
                if query.method == "INSERT":
                    sql_query, select_to_reverse = query.to_sql()
                    result.append(self.create_reverse_query(query))
                    self._insert(sql_query)
                elif query.method == "DELETE":
                    sql_query, select_to_reverse = query.to_sql()
                    stmt = text(select_to_reverse)
                    result_proxy = self.database_connection.execute(stmt)
                    result_set = result_proxy.cursor.fetchall()
                    if len(result_set) != 0:
                        result.append(self.create_reverse_query(query, result_set))
                    self._delete(sql_query)
                else:
                    sql_query, select_to_reverse = query.to_sql()
                    stmt = text(select_to_reverse)
                    result_proxy = self.database_connection.execute(stmt)
                    result_set = result_proxy.cursor.fetchall()
                    if len(result_set) != 0:
                        result.append(self.create_reverse_query(query, result_set))
                    self._update(sql_query)
            except:
                self.logger.error("Transaction failed!")
                raise TransactionException
        return result

    def rollback(self):
        self.app.logger.warning("Performing transaction rollback")
        self.database_connection.rollback()
        return jsonify(success=True)

    def commit(self):
        self.app.logger.info("Performing transaction commit")
        try:
            self.database_connection.commit()
        except TransactionException:
            raise TransactionException

    @staticmethod
    def create_reverse_query(transaction, values=None):
        if values is None:
            values = {}
        if transaction.method == "INSERT":
            where = ""
            column_names = list(transaction.values.keys())
            old_values = list(transaction.values.values())
            for i in range(0, len(old_values)):
                where += str(column_names[i]) + "=" + str(old_values[i]) + " AND "
            where = where[:-4]

            result = "DELETE FROM " + transaction.table_name + " WHERE " + where

            return result
        elif transaction.method == "UPDATE":
            update_elements = []
            old_columns = list(transaction.values.keys())
            for j in range(0, len(values)):
                result = "UPDATE " + transaction.table_name + " SET "
                for i in range(0, len(values[j])):
                    if isinstance(values[j][i], int):
                        result += str(old_columns[i]) + "=" + str(values[j][i]) + ","
                    else:
                        result += str(old_columns[i]) + "='" + str(values[j][i]) + "',"
                result = result[:-1]

                if transaction.where is not None:
                    result += " WHERE " + transaction.where
                update_elements.append(result)
            return update_elements
        else:
            insert_elements = []
            for j in range(0, len(values)):
                result = "INSERT INTO " + transaction.table_name + " VALUES ("
                for i in range(0, len(values[j])):
                    if isinstance(values[j][i], int):
                        result += str(values[j][i]) + ","
                    else:
                        result += "'" + values[j][i] + "',"
                result = result[:-1]
                result += ")"
                insert_elements.append(result)
            return insert_elements

    def reverse(self, statement):
        self.database_connection.execute(text(statement))


class RepoCoordinator:
    def __init__(self, repository: Repository):
        self.repository = repository

    def rollback(self):
        try:
            self.repository.rollback()
        except:
            return False
        return True

    def commit(self):
        try:
            self.repository.commit()
        except:
            return False
        return True

    def execute_transaction(self, transaction):
        if 'statements' in transaction.keys():
            try:
                content = json.loads(transaction['statements'])
                statements = []
                for statement in content:
                    statements.append(
                        Query(
                            method=statement['method'],
                            table_name=statement['table_name'],
                            values=_get_values(statement),
                            where=_get_where(statement)
                        )
                    )
                reverse_queries = self.repository.execute_statement(statements)
                return reverse_queries
            except IntegrityError:
                return jsonify(success=False)
        elif 'reverse' in transaction.keys():
            reverse = transaction['reverse']
            self._execute_reverse(reverse)
        else:
            return jsonify(success=False)

    def _execute_reverse(self, transactions):
        for query in transactions:
            if isinstance(query, list):
                for subquery in query:
                    self.repository.reverse(subquery)
            else:
                self.repository.reverse(query)
        self.repository.commit()
        self.repository.database_connection.close()


def _get_values(statement):
    try:
        values_dict = {}
        values = statement['values']
        for key, value in values.items():
            values_dict[key] = value
        return values_dict
    except:
        return {}


def _get_where(statement):
    try:
        return statement['where']
    except:
        return None
