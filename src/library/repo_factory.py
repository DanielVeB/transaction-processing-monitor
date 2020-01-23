import logging

from flask_sqlalchemy import SQLAlchemy

from src.library.repos import Repository

REPO_TYPES = {
    "mysql": "mysql://",
    "postgres": "postgresql://",
    "oracle": "oracle://"
}


class Connection:
    def __init__(self, prefix):
        self.prefix = prefix + "://"

    def create_connection(self, connection, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.prefix + connection
        return SQLAlchemy(app)


class RepoFactory:
    logger = logging.getLogger(__name__)

    def __init__(self, app):
        self.app = app

    def create_repository(self, database_type, connection_uri):
        database_type = database_type.lower()
        if database_type in REPO_TYPES:
            database_connection = Connection(database_type).create_connection(connection_uri, self.app)
            return Repository(database_connection)
        else:
            RepoFactory.logger.error("Given database type is not supported!")
            raise NotImplementedError("Given database type is not supported!")
