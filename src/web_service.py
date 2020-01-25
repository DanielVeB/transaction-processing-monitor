import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.library.interfaces import IWebService
from src.library.repos import Repository

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)


class WebService(IWebService):
    logger = logging.getLogger(__name__)

    def __init__(self, uri=None, db_name=None, username=None, pwd=None, db_type="mysql", db_uri="localhost",
                 port=":3306"):
        self.uri = uri if uri is not None else db_type + "://" \
                                               + username + ":" + pwd + "@" \
                                               + db_uri + port + "/" + db_name

    def create_repository(self, db_app):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.uri
        database_connection = SQLAlchemy(db_app)
        return Repository(database_connection, db_app)


uri = "postgres://gmavcrpg:k0fO5TZwnQrXFh7e8Q2lcJOZYjAgaT3g@rajje.db.elephantsql.com:5432/gmavcrpg"
webservice = WebService(uri)
repository = webservice.create_repository(app)


# Transaction request
@app.route('/database/transaction', methods=['POST'])
def execute_transaction():
    transaction = request.get_json()
    result = repository.execute_statement(transaction)
    return jsonify(result)


# Should this methods have jsonify return?
# Commit
@app.route('/database/commmit', methods=['POST'])
def commit():
    result = repository.commit()
    return result


# Rollback
@app.route('/database/rollback', methods=['POST'])
def rollback():
    result = repository.rollback()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9234)
