from abc import abstractmethod, ABC


class IWebService(ABC):

    @abstractmethod
    def create_repository(self, connection_uri, app): raise NotImplementedError

    @abstractmethod
    def execute_transaction(self, connection_uri): raise NotImplementedError

    @abstractmethod
    def commit(self, connection_uri): raise NotImplementedError

    @abstractmethod
    def rollback(self, connection_uri): raise NotImplementedError
