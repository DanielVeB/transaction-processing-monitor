import abc


class IRepository(abc.ABC):
    @abc.abstractmethod
    def add(self):
        pass

    @abc.abstractmethod
    def remove(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass
