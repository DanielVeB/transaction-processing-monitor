from abc import abstractmethod, ABC


class IRepository(ABC):
    @abstractmethod
    def get(self, item): raise NotImplementedError

    @abstractmethod
    def insert(self, item): raise NotImplementedError

    @abstractmethod
    def delete(self, item): raise NotImplementedError
