import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from src.library.interfaces import IDatabaseService
from src.library.repos import Repository


class DatabaseService(IDatabaseService):
    logger = logging.getLogger(__name__)

    def __init__(self, flask_server, url=None, db_name=None, username=None, pwd=None, db_type="mysql",
                 db_uri="localhost",
                 port=":3306"):
        self.url = url if url is not None else db_type + "://" \
                                               + username + ":" + pwd + "@" \
                                               + db_uri + port + "/" + db_name
        self.flask_server = flask_server
        self.repository = None

    def create_repository(self):
        self.flask_server.config['SQLALCHEMY_DATABASE_URI'] = self.url
        database_connection = SQLAlchemy(self.flask_server)
        engine = database_connection.engine
        self.repository = Repository(sessionmaker(autocommit=False,
                                                  autoflush=False,
                                                  bind=engine), self.flask_server)
        return self.repository
