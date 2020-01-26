from unittest import TestCase

from src.logic.request import Query


class TestTransaction(TestCase):
    def test_toSQL_insert(self):
        test = Query(method="INSERT",
                     table_name="myTable",
                     values={"name": "testName", "second_name": "xd", "age": 21}
                     )
        self.assertEqual(test.to_sql()[0], "INSERT INTO myTable(name,second_name,age) VALUES 'testName','xd',21")

    def test_toSQL_update(self):
        test = Query(method="UPDATE",
                     table_name="myTable",
                     values={"age": 21},
                     where="age < 40"
                     )
        self.assertEqual(test.to_sql()[0], "UPDATE myTable SET age = 21 WHERE age < 40")

    def test_toSQL_delete(self):
        test = Query(method="DELETE",
                     table_name="myTable",
                     values={},
                     where="age < 40"
                     )
        self.assertEqual(test.to_sql()[0], "DELETE FROM myTable WHERE age < 40")
