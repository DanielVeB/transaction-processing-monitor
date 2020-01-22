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
        result = ""

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

        else:
            result = "DELETE FROM " + self.table_name + " WHERE " + self.where
        return result