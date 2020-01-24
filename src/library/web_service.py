import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from src.library.interface_web_service import IWebService
from src.library.repos import Repository

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
app = Flask(__name__)


class WebService(IWebService):
    logger = logging.getLogger(__name__)

    def __init__(self, db_name, username, pwd, db_type="mysql", db_uri="localhost", port=":3306"):
        self.uri = db_type + "://" + username + ":" + pwd + "@" + db_uri + port + "/" + db_name
        self.repository = self.create_repository(self.uri)

    def create_repository(self, connection_uri):
        app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
        database_connection = SQLAlchemy(app)
        return Repository(database_connection, app)

    # Transaction request
    @app.route('/database/transaction', methods=['POST'])
    def execute_transaction(self):
        transaction = request.get_json()
        result = self.repository.execute_statement(transaction)
        return jsonify(result)

    # Should this methods have jsonify return?
    # Commit
    @app.route('/database/commmit', methods=['POST'])
    def commit(self):
        result = self.repository.commit()
        return result

    # Rollback
    @app.route('/database/rollback', methods=['POST'])
    def rollback(self):
        result = self.repository.rollback()
        return result

    @staticmethod
    def run_web_service(port):
        app.run(host='0.0.0.0', port=port)


webservice = WebService("test", "root", "lukasz")
if __name__ == '__main__':
    webservice.run_web_service(8081)