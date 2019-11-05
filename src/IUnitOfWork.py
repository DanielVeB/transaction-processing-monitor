from abc import abstractmethod


class IUnitOfWork:
    @abstractmethod
    def registerNew(self): raise NotImplementedError

    @abstractmethod
    def registerDirty(self): raise NotImplementedError

    @abstractmethod
    def registerClean(self): raise NotImplementedError

    @abstractmethod
    def registerDelete(self): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
