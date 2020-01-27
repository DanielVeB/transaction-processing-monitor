import logging

from flask import Flask, request, jsonify

from src.library.database_config import DatabaseService

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)

url = "postgres://gmavcrpg:k0fO5TZwnQrXFh7e8Q2lcJOZYjAgaT3g@rajje.db.elephantsql.com:5432/gmavcrpg"
database_service = DatabaseService(app, url)
repository = database_service.create_repository()


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
