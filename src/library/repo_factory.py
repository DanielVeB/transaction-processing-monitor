import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

REPO_TYPES = {
    "mysql": "mysql://",
    "postgres": "postgresql://",
    "oracle": "oracle://"
}


class Connection:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_connection(self, connection):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = self.prefix + connection
        return SQLAlchemy(app)


class RepoFactory:
    logger = logging.getLogger(__name__)

    @staticmethod
    def create_repository(database_type, connection_uri):
        database_type = database_type.lower()
        if database_type in REPO_TYPES:
            return Connection(database_type).create_connection(connection_uri)
        else:
            RepoFactory.logger.error("Given database type is not supported!")
            raise NotImplementedError("Given database type is not supported!")
