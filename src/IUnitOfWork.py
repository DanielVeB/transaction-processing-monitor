from abc import abstractmethod


class IUnitOfWork:
    @abstractmethod
    def registerNew(self): raise NotImplementedError
    def registerDirty(self): raise NotImplementedError
    def registerClean(self): raise NotImplementedError
    def registerDelete(self): raise NotImplementedError
    def commit(self): raise NotImplementedError
    def rollback(self): raise NotImplementedError
