from abc import abstractmethod, ABC


class IWebService(ABC):

    @abstractmethod
    def create_repository(self, db_app): raise NotImplementedError
