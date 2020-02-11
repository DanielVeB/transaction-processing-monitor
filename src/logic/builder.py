from abc import ABC, abstractmethod

from src.logic.request import Query


class QueryDirector:
    __builder = None

    def set_builder(self, builder):
        self.__builder = builder

    def get_query(self):
        method = self.__builder.get_method()
        table_name = self.__builder.get_table_name()
        values = self.__builder.get_values()
        where = self.__builder.get_where()
        return Query(method, table_name, values, where)


class Builder(ABC):

    @abstractmethod
    def get_method(self):
        raise NotImplementedError

    @abstractmethod
    def get_table_name(self):
        raise NotImplementedError

    @abstractmethod
    def get_values(self):
        raise NotImplementedError

    @abstractmethod
    def get_where(self):
        raise NotImplementedError


class QueryData(Builder):
    _table_name = None
    _values = dict()
    _where = None

    def __init__(self, method):
        self.method = method

    def with_table_name(self, table_name):
        self._table_name = table_name
        return self

    def with_values(self, values):
        self._values = values
        return self

    def with_where(self, where):
        self._where = where
        return self

    def get_table_name(self):
        return self._table_name

    def get_values(self):
        return self._values

    def get_where(self):
        return self._where

    def get_method(self):
        return self.method


class InsertQueryBuilder(QueryData):
    method = "INSERT"

    def __init__(self):
        super().__init__(self.method)


class UpdateQueryBuilder(QueryData):
    method = "UPDATE"

    def __init__(self):
        super().__init__(self.method)


class DeleteQueryBuilder(QueryData):
    method = "DELETE"

    def __init__(self):
        super().__init__(self.method)
