import json
from collections import namedtuple


def json_to_obj(data):
    return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


"""
data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
x = json2obj(data)
print(x.name)
"""
