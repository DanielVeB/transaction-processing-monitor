import logging

from flask_sqlalchemy import SQLAlchemy

from src.library.repos import Repository


class RepoFactory:
    logger = logging.getLogger(__name__)

    def __init__(self, app):
        self.app = app

    def create_repository(self, connection_uri):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
        database_connection = SQLAlchemy(self.app)
        return Repository(database_connection)
