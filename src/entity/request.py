from dataclasses import dataclass


@dataclass
class DP_Statement:
    # INSERT, UPDATE or DELETE
    method : str
    table_name : str
    # field_name : value
    values : {}
    # SQL statement
    where : str = None

    def toSQL(self):
        return "TODO"