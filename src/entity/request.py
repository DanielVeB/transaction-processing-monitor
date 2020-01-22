from dataclasses import dataclass
from uuid import UUID


@dataclass
class DP_Transaction:
    id : UUID
    statements : []

    def toString(self):
        return "Database with id" + str(self.id) + "statements: " + str(self.statements)

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
        result = ""
        select = ""

        if self.method == "INSERT":
            keys = ','.join(self.values.keys())
            values = list(self.values.values())
            result = self.method + " INTO " + self.table_name + "(" + keys + ")" + " VALUES "
            for i in range(0,len(values)):
                if isinstance(values[i],int):
                    result += str(values[i]) + ","
                else:
                    result += "'" + values[i] + "',"
            result = result[:-1]
            if self.where != None:
                result += " WHERE " + self.where

        elif self.method == "UPDATE":
            keys = list(self.values.keys())
            values = list(self.values.values())
            result = self.method + " " + self.table_name + " SET "
            for i in range(0, len(values)):
                if isinstance(values[i], int):
                    result += keys[i] + " = " + str(values[i]) + ","
                else:
                    result += keys[i] + " = '" + values[i] + "',"
            result = result[:-1]
            if self.where != None:
                result += " WHERE " + self.where
            keys = ','.join(self.values.keys())
            select = "SELECT " + keys + " FROM " + self.table_name
        else:
            keys = ','.join(self.values.keys())
            result = "DELETE FROM " + self.table_name + " WHERE " + self.where
            select = "SELECT " + keys +  " FROM " + self.table_name

        return result,select