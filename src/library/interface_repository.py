from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    def _update(self, request): raise NotImplementedError

    @abstractmethod
    def _insert(self, request): raise NotImplementedError

    @abstractmethod
    def _delete(self, request): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
