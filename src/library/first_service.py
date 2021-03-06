import logging

from flask import Flask, request, jsonify

from src.library.database_config import DatabaseService
from src.library.repos import RepoCoordinator

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)

url = "mysql://root@localhost:3306/test"
database_service = DatabaseService(app, url)
repoCoordinator = RepoCoordinator(database_service.create_repository())


@app.route('/execute', methods=['POST'])
def execute_transaction():
    content = request.get_json()
    result = repoCoordinator.execute_transaction(content)
    return jsonify(result)


# Commit
@app.route('/commit', methods=['POST'])
def commit():
    repoCoordinator.commit()
    return jsonify(success=True)


# Rollback
@app.route('/rollback', methods=['POST'])
def rollback():
    repoCoordinator.rollback()
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9035, debug=True)
