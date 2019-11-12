from abc import abstractmethod


class IUnitOfWork:
    @abstractmethod
    def register_new(self): raise NotImplementedError

    @abstractmethod
    def register_dirty(self): raise NotImplementedError

    @abstractmethod
    def register_clean(self): raise NotImplementedError

    @abstractmethod
    def register_delete(self): raise NotImplementedError

    @abstractmethod
    def commit(self): raise NotImplementedError

    @abstractmethod
    def rollback(self): raise NotImplementedError
