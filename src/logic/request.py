from json import JSONEncoder
from uuid import UUID

from dataclasses import dataclass

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


@dataclass
class Query:
    # INSERT, UPDATE or DELETE
    method: str
    table_name: str
    # field_name : value
    values: {}
    # SQL statement
    where: str = None

    def to_sql(self):
        result = ""
        select = ""

        if self.method == "INSERT":
            keys = ','.join(self.values.keys())
            values = list(self.values.values())
            result = self.method + " INTO " + self.table_name + "(" + keys + ")" + " VALUES ("
            for i in range(0, len(values)):
                if isinstance(values[i], int):
                    result += str(values[i]) + ","
                else:
                    result += "'" + values[i] + "',"
            result = result[:-1]
            result += ") "
            if self.where is not None:
                result += " WHERE " + self.where

        elif self.method == "UPDATE":
            keys = list(self.values.keys())
            values = list(self.values.values())
            result = self.method + " " + self.table_name + " SET "
            for i in range(0, len(values)):
                if isinstance(values[i], int):
                    result += keys[i] + "=" + str(values[i]) + ","
                else:
                    result += keys[i] + "='" + values[i] + "',"
            result = result[:-1]
            if self.where is not None:
                result += " WHERE " + self.where
            keys = ','.join(self.values.keys())
            select = "SELECT " + keys + " FROM " + self.table_name + " WHERE " + self.where
        else:
            keys = ','.join(self.values.keys())
            result = "DELETE FROM " + self.table_name + " WHERE " + self.where
            select = "SELECT * FROM " + self.table_name + " WHERE " + self.where

        return result, select


@dataclass
class QueryBuilder:
    # INSERT, UPDATE or DELETE
    _method: str
    _table_name: str
    # field_name : value
    _values: {}
    # SQL statement
    _where: str = None

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
        return Query(self._method, self._table_name, self._values, self._where)

class QueryEncoder(JSONEncoder):
    def default(self, query):
        return query.__dict__
