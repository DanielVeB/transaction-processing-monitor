import json
import logging

from flask import jsonify, abort
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, IntegrityError

from src.library.execptions import TransactionException
from src.library.interfaces import IRepository
from src.logic.request import Query, UpdateQuery, InsertQuery, DeleteQuery


class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, session, app):
        self.database_connection = session()
        self.app = app

    def _update(self, request):
        result = []
        update_query = UpdateQuery(request)
        sql_query, select_to_reverse = update_query.to_sql()
        stmt = text(select_to_reverse)
        result_proxy = self.database_connection.execute(stmt)
        result_set = result_proxy.cursor.fetchall()
        if len(result_set) != 0:
            result.append(update_query.reverse(result_set))
        self.logger.info("Updating row")
        stmt = text(sql_query)
        self.database_connection.execute(stmt)
        return result

    def _insert(self, request):
        result = []
        insert_query = InsertQuery(request)
        sql_query = insert_query.to_sql()
        result.append(insert_query.reverse(None))
        self.logger.info("Inserting row")
        stmt = text(sql_query)
        self.database_connection.execute(stmt)
        return result

    def _delete(self, request):
        result = []
        delete_query = DeleteQuery(request)
        sql_query, select_to_reverse = delete_query.to_sql()
        stmt = text(select_to_reverse)
        result_proxy = self.database_connection.execute(stmt)
        result_set = result_proxy.cursor.fetchall()
        if len(result_set) != 0:
            result.append(delete_query.reverse(result_set))
        self.logger.info("Deleting row")
        stmt = text(request)
        self.database_connection.execute(stmt)
        return result

    def execute_statement(self, transaction):
        result = []
        for query in transaction:
            try:
                if query.method == "INSERT":
                    result += self._insert(query)
                elif query.method == "DELETE":
                    result += self._delete(query)
                else:
                    result += self._update(query)
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
        except (TransactionException, OperationalError):
            raise TransactionException

    def reverse(self, statement):
        self.database_connection.execute(text(statement))


class RepoCoordinator:
    def __init__(self, repository: Repository):
        self.repository = repository

    def rollback(self):
        try:
            self.repository.rollback()
        except IntegrityError:
            return abort(500)

    def commit(self):
        try:
            self.repository.commit()
        except IntegrityError:
            return abort(500)

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
                abort(500)
        elif 'reverse' in transaction.keys():
            reverse = transaction['reverse']
            self._execute_reverse(reverse)
        else:
            abort(500)

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
