import json

from src.logic.request import Query, QueryEncoder

query1 = Query("INSERT", "test", [{"id": 60, "value": 60}])
query2 = Query("DELETE", "test", [{"id": 30, "value": 40}])

test = [query1, query2]
json_to_send = json.dumps(test, cls=QueryEncoder)

json_received = json.loads(json_to_send)

print("Finito")
