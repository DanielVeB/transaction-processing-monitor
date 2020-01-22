from unittest import TestCase

from src.entity.request import DP_Statement


class TestDP_Statement(TestCase):
    def test_toSQL(self):
        test = DP_Statement(method= "INSERT",
                            table_name="myTable",
                            values= {"name": "testName","second_name": "xd", "age": 21}
                            )
        self.assertEqual(test.toSQL(), "INSERT INTO myTable(name, second_name,age) VALUES 'testName','xd',21")