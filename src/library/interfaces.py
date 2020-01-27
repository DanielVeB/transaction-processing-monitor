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


class IDatabaseService(ABC):

    @abstractmethod
    def create_repository(self): raise NotImplementedError


class IUnitOfWork(ABC):

    @abstractmethod
    def add_service(self, repo): raise NotImplementedError

    @abstractmethod
    def delete_service(self, repo): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def _rollback(self): raise NotImplementedError
