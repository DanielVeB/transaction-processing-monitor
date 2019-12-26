from abc import ABC, abstractmethod

from src.logic.commands import Command


class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @staticmethod
    def get_item(item):
        return item


class InsertAction(Action):
    def __init__(self, item, repo):
        self.item = item
        self.action = Command.INSERT
        self.repo = repo

    def execute(self):
        self.repo.insert(self.item)


class UpdateAction(Action):
    def __init__(self, item, changes, repo):
        self.item = item
        self.old_item = item.clone()
        self.changes = changes
        self.action = Command.UPDATE
        self.repo = repo

    def execute(self):
        item = self.repo.get(self.item)
        # some changes


class DeleteAction(Action):
    def __init__(self, item, repo):
        self.item = item
        self.action = Command.DELETE
        self.repo = repo

    def execute(self):
        self.repo.delete(self.item)


class RestoreAction(Action):
    def __init__(self, item, old_item, repo):
        self.item = item
        self.old_item = old_item
        self.repo = repo

    def execute(self):
        item = self.repo.get(self.item)
        item = self.old_item
