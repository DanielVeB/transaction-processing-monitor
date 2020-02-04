import unittest
from unittest import mock

import requests

# This is the class we want to test
from src.logic.webservices import WebServiceBuilder
from src.logic.coordinator import Coordinator
from src.logic.request import Query


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


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
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

    @mock.patch('requests.post', side_effect=mocked_requests_get)
    def test_flow(self, mock_get):
        coordinator = Coordinator()
        coordinator.add_service(WebServiceTestClass.webservice_first)
        WebServiceTestClass.webservice_first.add_query(Query("INSERT", "test", {"key": "value"}))
        try:
            coordinator.execute_transaction()
            coordinator.commit()
        except:
            self.fail("Coordinator raised ExceptionType unexpectedly!")


if __name__ == '__main__':
    unittest.main()
