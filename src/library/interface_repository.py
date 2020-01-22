from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    def update(self, table, new_values): raise NotImplementedError

    @abstractmethod
    def insert(self, table, values): raise NotImplementedError

    @abstractmethod
    def delete(self, table, conditions): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
