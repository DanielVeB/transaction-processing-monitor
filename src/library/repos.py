import json
import logging
from abc import ABC, abstractmethod

from flask import jsonify, abort
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, IntegrityError

from src.library.command import InsertCommand, UpdateCommand, DeleteCommand
from src.library.execptions import TransactionException
from src.library.interfaces import IRepository
from src.logic.request import Query



class Repository(IRepository):
    logger = logging.getLogger(__name__)

    def __init__(self, session, app):
        self.database_connection = session()
        self.app = app

    def update(self, request):
        self.logger.info("Updating row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def insert(self, request):
        self.logger.info("Inserting row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def delete(self, request):
        self.logger.info("Deleting row")
        stmt = text(request)
        self.database_connection.execute(stmt)

    def execute(self, query):
        return self.database_connection.execute(query)

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
        self.commands = []
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
                commands = []
                for statement in content:
                    query = self.get_Query(statement)
                    try:
                        command = self.get_command(query)
                        commands.append(command)
                        command.execute()
                    except:
                        self.logger.error("Transaction failed!")
                        break
                #
                #  what's next....
                #

                # reverse_queries = self.repository.execute_statement(statements)
                # return reverse_queries
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

    def get_Query(self, statement):
        return Query(
            method=statement['method'],
            table_name=statement['table_name'],
            values=_get_values(statement),
            where=_get_where(statement)
        )

    def get_command(self,query):
        if query.method == "INSERT":
            return InsertCommand(query)

        elif query.method == "UPDATE":
            return UpdateCommand(query)

        elif query.method == "DELETE":
            return DeleteCommand(query)

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
