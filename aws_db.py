# Example
import logging

from flask import Flask, request, jsonify

from src.library.database_config import DatabaseService

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

app = Flask(__name__)
URL = "mysql://admin:admin1234@transaction-moniotr.cyijtv3eudvp.eu-west-2.rds.amazonaws.com:3306/test"
dbs = DatabaseService(app, URL)
repo = dbs.create_repository()


@app.route('/execute', methods=['POST'])
def execute():
    content = request.get_json()
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=content), 200


@app.route('/commit', methods=['POST'])
def commit():
    content = request.get_json()
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=content), 200


@app.route('/rollback', methods=['POST'])
def rollback():
    content = request.get_json()
    return jsonify(isError=False,
                   message="Success",
                   statusCode=200,
                   data=content), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9019)
