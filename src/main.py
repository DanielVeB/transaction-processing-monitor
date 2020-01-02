import sys

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields

import logging

from src.dto.resource import DpResource
from src.logic.coordinator import Coordinator

app = Flask(__name__)
api = Api(app=app)

ns_repo = api.namespace('repository', description='')
ns_transactions = api.namespace('transaction', description='')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# json models

repository_dto = \
    ns_repo.model(name="repo",
                  model={
                      "type": fields.String(description="type of repository, possible values:"
                                                        "\nMySQL"
                                                        "\nPostgreSQL"
                                                        "\nSQLite",
                                            example="MySQL",
                                            required=True),
                      "host": fields.String(description="", example="53.231.57.128"),
                      "port": fields.String(description="", example="12017"),
                      "user": fields.String(description="", example="user"),
                      "password": fields.String(description="", example="password"),
                  })

transaction_dto = ns_transactions.model(name="transaction",
                                        model={
                                            "repo_id": fields.String(
                                                description="Unique identifier of repository",
                                                required=True,
                                                example="531da-3123a-54fdcb-125ab"
                                            ),
                                            "operation_type": fields.String(
                                                description="Type of operation, possible values:"
                                                            "\nINSERT"
                                                            "\nGET"
                                                            "\nDELETE",
                                                required=True,
                                                example="INSERT"
                                            ),
                                            "object": fields.String(
                                                description="object on which the operation will be executed"

                                            )
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
    @ns_repo.expect([repository_dto], validate=True )
    def put(self):
        """Add repository"""
        data = request.get_json()
        resources = []
        for resource in data:
            resources.append(DpResource(
                host=resource.get('host'),
                port=resource.get('port'),
                user=resource.get('user'),
                password=resource.get('password')
            ))
        print(resources[0].id)
        pass


@ns_transactions.route('/<int:id>')
@ns_transactions.param('id', 'The transaction identifier')
class TransactionController(Resource):

    @ns_transactions.doc()
    def delete(self, id):
        """Delete transaction with given id"""
        logging.info("Delete repository with id " + str(id))
        # coordinator.delete_repository(id)
        return id


@ns_transactions.route('')
class AddTransactions(Resource):

    @ns_transactions.doc()
    @ns_transactions.expect([transaction_dto],validate=True)
    def put(self):
        """Add transaction(s) """
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
