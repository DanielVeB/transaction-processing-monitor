from abc import abstractmethod


class IRepository:
    @abstractmethod
    def get_all(self): raise NotImplementedError

    @abstractmethod
    def get(self, id): raise NotImplementedError

    @abstractmethod
    def create(self, item): raise NotImplementedError

    @abstractmethod
    def update(self, item): raise NotImplementedError

    @abstractmethod
    def delete(self, id): raise NotImplementedError
