import sys

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields

import logging

from src.dto.resource import DpResource
from src.logic.coordinator import Coordinator

app = Flask(__name__)
api = Api(app=app)

ns_resource = api.namespace('repository', description='')
ns_transactions = api.namespace('transaction', description='')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# json models

repository_dto = \
    ns_resource.model(name="resource",
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
                                                example="GET"
                                            ),
                                            "object": fields.String(
                                                description="",
                                                example="{'user':'User'"
                                                        ",'field1': 'val1' }",
                                                required=False),
                                            "where_condition": fields.String(
                                                description="For update,delete and get operation. You have to write "
                                                            "here correct condition after WHERE clause",
                                                example="age BETWEEN 20 AND 26",
                                                required=False
                                            )
                                        })

coordinator = Coordinator()


class Invalid_ID(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(Invalid_ID)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@ns_resource.route('/<string:id>')
@ns_resource.param('id', 'The repository identifier')
class Repository(Resource):

    @ns_resource.doc()
    @ns_resource.response(404, "NOT FOUND")
    @ns_resource.response(200, "SUCCESS")
    def delete(self, id):
        """Delete resource with given id"""
        logging.info("Delete resource with id " + id)
        answer = coordinator.delete_repository(id)
        if answer is None:
            raise Invalid_ID("Resource with id " + id + " not found", 404)
        return answer.serialize()

    @ns_resource.doc()
    @ns_resource.response(404, "NOT FOUND")
    @ns_resource.response(200, "SUCCESS")
    def get(self, id):
        """Return information about repository"""
        logging.info("Get resource with id " + str(id))
        answer = coordinator.get_repository(id)
        if answer is None:
            raise Invalid_ID("Resource with id " + str(id) + " not found", 404)
        return answer.serialize()


@ns_resource.route('')
class AddRepository(Resource):

    @ns_resource.doc()
    @ns_resource.expect([repository_dto], validate=True)
    def put(self):
        """Add resource"""
        data = request.get_json()
        resources = []
        for resource in data:
            resources.append(DpResource(
                host=resource.update('host'),
                port=resource.update('port'),
            ))
        repo_id = coordinator.add_repository(resources)
        return "Added repo with id: " + repo_id

    @ns_resource.doc()
    def get(self):
        """Get all resources"""
        repos = coordinator.get_all_repositories()
        json_repos = dict()
        for repo in repos:
            json_repos[repo] = repos[repo].serialize()
        return json_repos


@ns_transactions.route('/<string:id>')
@ns_transactions.param('id', 'The transaction identifier')
class TransactionController(Resource):

    @ns_transactions.doc()
    def delete(self, id):
        """Delete transaction with given id"""
        logging.info("Delete repository with id " + id)
        coordinator.delete_repository(id)
        return id


@ns_transactions.route('')
class AddTransactions(Resource):

    @ns_transactions.doc()
    @ns_transactions.expect([transaction_dto], validate=True)
    def put(self):
        """Add transaction(s) """
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
