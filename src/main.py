import sys

from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields

import logging

from src.logic.coordinator import Coordinator

app = Flask(__name__)
api = Api(app=app)

ns_repo = api.namespace('repository', description='')
ns_transactions = api.namespace('transaction', description='')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# json models

insert_repository = ns_repo.model(name="repo",
                                  model={
    "type": fields.String(description= "type of repository, possible values:"
                                       "\nMySQL"
                                       "\nPostgreSQL"
                                       "\nSQLite",
                          example="MySQL", required= True ),
    "host": fields.String(description = "", example="53.231.57.128"),
    "port": fields.String(description = "", example="12017"),
    "user": fields.String(description = "", example="user"),
    "database": fields.String(description = "", example="password"),
})

coordinator = Coordinator()


@ns_repo.route('/<int:id>')
@ns_repo.param('id', 'The repository identifier')
class Repository(Resource):

    @ns_repo.doc()
    def delete(self, id):
        """Delete repository with given id"""
        return id

    @ns_repo.doc()
    def get(self, id):
        """Return information about repository"""
        return id


@ns_repo.route('')
class AddRepository(Resource):

    @ns_repo.doc()
    @ns_repo.expect([insert_repository])
    def put(self):
        """Return information about repository"""
        return id


@ns_transactions.route('/<int:id>')
@ns_transactions.param('id', 'The transaction identifier')
class TransactionController(Resource):

    @ns_transactions.doc()
    def delete(self, id):
        """Delete transaction with given id"""
        logging.info("Delete repository with id " + str(id))
        # coordinator.delete_repository(id)
        return id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
