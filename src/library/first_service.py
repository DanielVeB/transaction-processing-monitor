import logging

from flask import Flask, request, jsonify

from src.library.database_config import DatabaseService
from src.library.repos import RepoCoordinator

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)

url = "mysql://admin:admin1234@transaction-moniotr.cyijtv3eudvp.eu-west-2.rds.amazonaws.com:3306/test"
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
    result = repoCoordinator.commit()
    return jsonify(success=result)


# Rollback
@app.route('/rollback', methods=['POST'])
def rollback():
    result = repoCoordinator.rollback()
    return jsonify(success=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9035, debug=True)
