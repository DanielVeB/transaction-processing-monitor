from unittest import TestCase

from src.entity.request import DP_Statement


class TestDP_Statement(TestCase):
    def test_toSQL(self):
        test = DP_Statement(method= "INSERT",
                            table_name="myTable",
                            values= {"name": "testName","second_name": "xd", "age": 21}
                            )
        self.assertEqual(test.toSQL()[0], "INSERT INTO myTable(name,second_name,age) VALUES 'testName','xd',21")

    def test_update(self):
        test = DP_Statement(method="UPDATE",
                            table_name="myTable",
                            values={"age": 21},
                            where= "age < 40"
                            )
        self.assertEqual(test.toSQL()[0], "UPDATE myTable SET age = 21 WHERE age < 40")