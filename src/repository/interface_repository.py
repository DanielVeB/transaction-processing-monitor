from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    def get_all(self): raise NotImplementedError

    @abstractmethod
    def get(self, item): raise NotImplementedError

    @abstractmethod
    def create(self, item): raise NotImplementedError

    @abstractmethod
    def delete(self, item): raise NotImplementedError
