from abc import abstractmethod, ABC


class IUnitOfWork(ABC):

    @abstractmethod
    def add_service(self, repo): raise NotImplementedError

    @abstractmethod
    def delete_service(self, repo): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def _rollback(self): raise NotImplementedError
