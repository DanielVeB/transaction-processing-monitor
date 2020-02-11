from src.logic.coordinator import Coordinator
from src.logic.request import QueryBuilder
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()

first_webservice = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9035") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

second_webservice = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9030") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

coordinator.add_service(first_webservice)
coordinator.add_service(second_webservice)

query_insert = QueryBuilder() \
    .with_method("INSERT") \
    .with_table_name("test") \
    .with_values({"idtest": 6787, "value": 999}) \
    .build()

query_delete = QueryBuilder() \
    .with_method("DELETE") \
    .with_table_name("test") \
    .with_where("idtest=77237") \
    .build()

first_webservice.add_query(query_insert)
second_webservice.add_query(query_insert)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")