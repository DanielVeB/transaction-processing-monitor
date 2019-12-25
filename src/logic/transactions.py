from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def execute(self, repo):
        raise NotImplementedError


class InsertAction(Action):
    def __init__(self, item):
        self.item = item

    def execute(self, repo):
        repo.insert(self.item)


class UpdateAction(Action):
    def __init__(self, item, changes):
        self.item = item
        self.changes = changes

    def execute(self, repo):
        item = repo.get(self.item)
        # some changes


class DeleteAction(Action):
    def __init__(self, item):
        self.item = item

    def execute(self, repo):
        repo.delete(self.item)
