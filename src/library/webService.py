import logging

from flask import Flask, request, jsonify

from src.library.connection_config import URI
from src.library.repo_factory import RepoFactory

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

repoFactory = RepoFactory(app)
webService = repoFactory.create_repository(URI)


# Transaction
@app.route('/database/transaction', methods=['POST'])
def execute_transaction():
    transaction = request.get_json()
    result = webService.execute_statement(transaction)
    return jsonify(result)

# Commit
@app.route('/database/commmit', methods=['POST'])
def commit():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
