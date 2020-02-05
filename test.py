import json

sql = "SELECT * FROM DATABASE"
sql2 = "ISNERT INTo WOPDA"

transactions = [sql, sql2]
json_form = json.dumps(transactions)
python_dictionary = json.loads(json_form)
print(python_dictionary[0])
