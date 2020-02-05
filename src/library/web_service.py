import json
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
    content['statements'] = json.loads(content['statements'])
    result = repoCoordinator.execute_transaction(content)
    return jsonify(result)


# Should this methods have jsonify return?
# Commit
@app.route('/commit', methods=['POST'])
def commit():
    result = repoCoordinator.commit()
    return result.status_code


# Rollback
@app.route('/rollback', methods=['POST'])
def rollback():
    result = repoCoordinator.rollback()
    return result.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9020, debug=True)
