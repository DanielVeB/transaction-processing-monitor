from dataclasses import dataclass
from uuid import UUID


@dataclass
class DP_Repository:
    host: str
    port: str
    endpoints: []


@dataclass
class DP_Transaction:
    id: UUID
    statements: []

    def toString(self):
        return "Database with id" + str(self.id) + "statements: " + str(self.statements)


@dataclass
class DP_Statement:
    # INSERT, UPDATE or DELETE
    method: str
    table_name: str
    # field_name : value
    values: {}
    # SQL statement
    where: str = None

    def toSQL(self):
        result = ""

        if self.method == "INSERT":
            keys = ','.join(self.values.keys())
            values = list(self.values.values())
            table = self.table_name + "(" + keys + ")"
            for i in range(0, len(values)):
                if isinstance(values[i], int):
                    result += str(values[i]) + ","
                else:
                    result += "'" + values[i] + "',"
            result = result[:-1]
            return table, result

        elif self.method == "UPDATE":
            keys = list(self.values.keys())
            values = list(self.values.values())
            for i in range(0, len(values)):
                if isinstance(values[i], int):
                    result += keys[i] + " = " + str(values[i]) + ","
                else:
                    result += keys[i] + " = '" + values[i] + "',"
            result = result[:-1]
            return self.table_name, result, self.where
        else:
            return self.table_name, self.where
