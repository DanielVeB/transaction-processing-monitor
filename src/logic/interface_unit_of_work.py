from abc import abstractmethod, ABC


class IUnitOfWork(ABC):

    @abstractmethod
    def add_repository(self, repo): raise NotImplementedError

    @abstractmethod
    def delete_repository(self, repo): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
