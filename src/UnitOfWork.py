from src.IUnitOfWork import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    def register_new(self):
        print("register_new")

    def register_dirty(self):
        print("register_dirty")

    def register_clean(self):
        print("register_clean")

    def register_delete(self):
        print("register_delete")

    def commit(self):
        print("commit")

    def rollback(self):
        print("rollback")