import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session

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
        self.repository = Repository(scoped_session(sessionmaker(autocommit=False,
                                                                 autoflush=False,
                                                                 bind=engine)), self.flask_server)
        return self.repository


# Example
app = Flask(__name__)

URL = "mysql://admin:admin1234@transaction-moniotr.cyijtv3eudvp.eu-west-2.rds.amazonaws.com:3306/test"
dbs = DatabaseService(app, URL)
repo = dbs.create_repository()

try:
    repo.database_connection.execute("Insert into tes values (100, 100)")
except:
    print("Failure")

repo.database_connection.commit()
