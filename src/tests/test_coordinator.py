import unittest
from unittest import mock

import requests

from src.library.repos import Repository
from src.logic.coordinator import Coordinator
from src.logic.request import Query
from src.logic.webservices import WebServiceBuilder


class WebServiceTestClass:
    webservice_first = WebServiceBuilder() \
        .with_host("localhost") \
        .with_port("8081") \
        .rollback_endpoint("/rollback") \
        .with_commit_endpoint("/commit") \
        .with_send_transaction_endpoint("/execute") \
        .build()

    def fetch_json(self, url):
        response = requests.get(url)
        return response.json()


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_response(*args, **kwargs):
    if args[0] == 'http://localhost:8081/execute':
        return MockResponse(Repository.create_reverse_query(args[1]), 200)

    return MockResponse(None, 404)


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://localhost:8081/execute':
        return MockResponse({"status": "Success"}, 200)
    elif args[0] == 'http://localhost:8081/commit':
        return MockResponse({"status": "Success"}, 200)

    return MockResponse(None, 404)


class CoordinatorTestClass(unittest.TestCase):
    def setUp(self):
        self.coordinator = Coordinator()
        self.coordinator.add_service(WebServiceTestClass.webservice_first)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_flow(self, mock_get):
        WebServiceTestClass.webservice_first.add_query(Query("INSERT", "test", {"key": "value"}))
        try:
            self.coordinator.execute_transaction()
            self.coordinator.commit()
        except:
            self.fail("Coordinator raised ExceptionType unexpectedly!")


if __name__ == '__main__':
    unittest.main()
