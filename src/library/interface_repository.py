from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    def _update(self, table, new_values, condition): raise NotImplementedError

    @abstractmethod
    def _insert(self, table, values): raise NotImplementedError

    @abstractmethod
    def _delete(self, table, condition): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
