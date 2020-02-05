import json

from flask import Flask
from sqlalchemy import text

from src.library.database_config import DatabaseService
from src.library.repos import RepoCoordinator
from src.logic.request import Query, QueryEncoder

query1 = Query("INSERT", "test", [{"id": 60, "value": 60}])
query2 = Query("DELETE", "test", [{"id": 30, "value": 40}])

test = [query1, query2]
json_to_send = json.dumps(test, cls=QueryEncoder)

json_received = json.loads(json_to_send)

app = Flask(__name__)
url = "mysql://admin:admin1234@transaction-moniotr.cyijtv3eudvp.eu-west-2.rds.amazonaws.com:3306/test"
database_service = DatabaseService(app, url)
repoCoordinator = RepoCoordinator(database_service.create_repository())

stmt = text("INSERT INTO test VALUES(73, 68)")
repoCoordinator.repository.database_connection.execute(stmt)
set_in_session = repoCoordinator.repository.database_connection.new
repoCoordinator.rollback()
