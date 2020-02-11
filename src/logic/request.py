from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import JSONEncoder
from uuid import UUID

from src.library.execptions import MissingParametersException


@dataclass
class Transaction:
    repository_id: UUID
    statements: []

    def toString(self):
        return "Database with id" + str(self.repository_id) + "statements: " + str(self.statements)

    def serialize(self):
        return {
            "repository_id": self.repository_id,
            "statements": ([s.serialize() for s in self.statements])
        }


class QueryInterface(ABC):
    @abstractmethod
    def reverse(self, old_data):
        raise NotImplementedError

    @abstractmethod
    def to_sql(self):
        raise NotImplementedError


class UpdateQuery(QueryInterface):
    def __init__(self, query):
        self.query = query

    def reverse(self, old_data):
        update_elements = []
        old_columns = list(self.query.values.keys())
        new_values = list(self.query.values.values())
        for j in range(0, len(old_data)):
            result = "UPDATE " + self.query.table_name + " SET "
            for i in range(0, len(old_data[j])):
                if isinstance(old_data[j][i], int):
                    result += str(old_columns[i]) + "=" + str(old_data[j][i]) + ","
                else:
                    result += str(old_columns[i]) + "='" + str(old_data[j][i]) + "',"
            result = result[:-1]

        where = ""
        for i in range(0, len(old_columns)):
            if isinstance(new_values[i], int):
                where += str(old_columns[i]) + "=" + str(new_values[i]) + " AND "
            else:
                where += str(old_columns[i]) + "='" + str(new_values[i]) + "' AND "
        where = where[:-4]
        result += " WHERE " + where
        update_elements.append(result)
        return update_elements

    def to_sql(self):
        keys = list(self.query.values.keys())
        values = list(self.query.values.values())
        result = self.query.method + " " + self.query.table_name + " SET "
        for i in range(0, len(values)):
            if isinstance(values[i], int):
                result += keys[i] + "=" + str(values[i]) + ","
            else:
                result += keys[i] + "='" + values[i] + "',"
        result = result[:-1]
        if self.query.where is not None:
            result += " WHERE " + self.query.where
        keys = ','.join(self.query.values.keys())
        select = "SELECT " + keys + " FROM " + self.query.table_name + " WHERE " + self.query.where

        return result, select


class InsertQuery(QueryInterface):
    def __init__(self, query):
        self.query = query

    def reverse(self, old_data):
        where = ""
        column_names = list(self.query.values.keys())
        old_values = list(self.query.values.values())
        for i in range(0, len(old_values)):
            where += str(column_names[i]) + "=" + str(old_values[i]) + " AND "
        where = where[:-4]

        result = "DELETE FROM " + self.query.table_name + " WHERE " + where

        return result

    def to_sql(self):
        keys = ','.join(self.query.values.keys())
        values = list(self.query.values.values())
        result = self.query.method + " INTO " + self.query.table_name + "(" + keys + ")" + " VALUES ("
        for i in range(0, len(values)):
            if isinstance(values[i], int):
                result += str(values[i]) + ","
            else:
                result += "'" + values[i] + "',"
        result = result[:-1]
        result += ") "
        if self.query.where is not None:
            result += " WHERE " + self.query.where

        return result


class DeleteQuery(QueryInterface):
    def __init__(self, query):
        self.query = query

    def reverse(self, old_data):
        insert_elements = []
        for j in range(0, len(old_data)):
            result = "INSERT INTO " + self.query.table_name + " VALUES ("
            for i in range(0, len(old_data[j])):
                if isinstance(old_data[j][i], int):
                    result += str(old_data[j][i]) + ","
                else:
                    result += "'" + old_data[j][i] + "',"
            result = result[:-1]
            result += ")"
            insert_elements.append(result)
        return insert_elements

    def to_sql(self):
        result = "DELETE FROM " + self.query.table_name + " WHERE " + self.query.where
        select = "SELECT * FROM " + self.query.table_name + " WHERE " + self.query.where
        return result, select


@dataclass
class Query:
    # INSERT, UPDATE or DELETE
    method: str
    table_name: str
    # field_name : value
    values: {}
    # SQL statement
    where: str = None


@dataclass
class QueryBuilder:
    _method: str = None
    _table_name: str = None
    _values: {} = None
    _where: str = ""

    def with_method(self, method):
        self._method = method
        return self

    def with_table_name(self, table_name):
        self._table_name = table_name
        return self

    def with_values(self, values):
        self._values = values
        return self

    def with_where(self, where):
        self._where = where
        return self

    def build(self):
        if vars(self).values() is None:
            raise MissingParametersException
        if self._where == "":
            self._where = None
        return Query(self._method, self._table_name, self._values, self._where)


class QueryEncoder(JSONEncoder):
    def default(self, query):
        return query.__dict__
