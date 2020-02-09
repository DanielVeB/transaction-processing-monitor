from src.logic.coordinator import Coordinator
from src.logic.request import QueryBuilder
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()

second_webservice = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9030") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

coordinator.add_service(second_webservice)

second_query = QueryBuilder() \
    .with_method("INSERT") \
    .with_table_name("test") \
    .with_values({"idtest": 7787, "value": 999}) \
    .build()

second_webservice.add_query(second_query)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")