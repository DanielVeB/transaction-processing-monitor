import logging
from abc import ABC, abstractmethod

from sqlalchemy import text


class Command(ABC):
    @abstractmethod
    def execute(self): pass

    @abstractmethod
    def abort(self): pass


class InsertCommand(Command):
    logger = logging.getLogger(__name__)

    def __init__(self, repository, query):
        self.repository = repository
        self.sql_query, self.select_to_reverse = query.to_sql()
        self.reverse_stmt = self.reverse(query)

    def execute(self):
        self.logger.info("Inserting row")
        self.repository.insert(self.sql_query)

    def abort(self):
        self.repository.reverse(self.reverse_stmt)

    @staticmethod
    def reverse(query):
        where = ""
        column_names = list(query.values.keys())
        old_values = list(query.values.values())
        for i in range(0, len(old_values)):
            where += str(column_names[i]) + "=" + str(old_values[i]) + " AND "
        where = where[:-4]
        result = "DELETE FROM " + query.table_name + " WHERE " + where
        return result


class UpdateCommand(Command):
    logger = logging.getLogger(__name__)

    def __init__(self, repository, query):
        self.reverse_stmt = []
        self.repository = repository
        self.sql_query, select_to_reverse = query.to_sql()
        stmt = text(select_to_reverse)
        result_proxy = self.repository.execute(stmt)
        result_set = result_proxy.cursor.fetchall()
        if len(result_set) != 0:
            self.reverse_stmt.append(self.reverse(query, result_set))

    def execute(self):
        self.logger.info("Updating row")
        self.repository.update(self.sql_query)

    def abort(self):
        for reverse_stmt in self.reverse_stmt:
            self.repository.reverse(reverse_stmt)

    @staticmethod
    def reverse(query, result_set):
        update_elements = []
        old_columns = list(query.values.keys())
        for j in range(0, len(result_set)):
            result = "UPDATE " + query.table_name + " SET "
            for i in range(0, len(result_set[j])):
                if isinstance(result_set[j][i], int):
                    result += str(old_columns[i]) + "=" + str(result_set[j][i]) + ","
                else:
                    result += str(old_columns[i]) + "='" + str(result_set[j][i]) + "',"
            result = result[:-1]

            if query.where is not None:
                result += " WHERE " + query.where
            update_elements.append(result)
        return update_elements


class DeleteCommand(Command):
    logger = logging.getLogger(__name__)

    def __init__(self, repository, query):
        self.reverse_stmt = []
        self.repository = repository
        self.sql_query, select_to_reverse = query.to_sql()
        stmt = text(select_to_reverse)
        result_proxy = self.repository.execute(stmt)
        result_set = result_proxy.cursor.fetchall()
        if len(result_set) != 0:
            self.reverse_stmt.append(self.reverse(query, result_set))

    def execute(self):
        self.repository.delete(self.sql_query)

    def abort(self):
        for reverse_stmt in self.reverse_stmt:
            self.repository.reverse(reverse_stmt)

    @staticmethod
    def reverse(query, result_set):
        insert_elements = []
        for j in range(0, len(result_set)):
            result = "INSERT INTO " + query.table_name + " VALUES ("
            for i in range(0, len(result_set[j])):
                if isinstance(result_set[j][i], int):
                    result += str(result_set[j][i]) + ","
                else:
                    result += "'" + result_set[j][i] + "',"
            result = result[:-1]
            result += ")"
            insert_elements.append(result)
        return insert_elements
