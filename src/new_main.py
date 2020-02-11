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

coordinator.add_service(second_webservice)
coordinator.add_service(first_webservice)

query_insert = QueryBuilder() \
    .with_method("INSERT") \
    .with_table_name("test") \
    .with_values({"idtest": 6785773, "value": 999}) \
    .build()

query_delete = QueryBuilder() \
    .with_method("DELETE") \
    .with_table_name("test") \
    .with_where("idtest=678577") \
    .build()

query_update = QueryBuilder() \
    .with_method("UPDATE") \
    .with_table_name("test") \
    .with_values({"value": 999}) \
    .with_where("value=567") \
    .build()

first_webservice.add_query(query_delete)
second_webservice.add_query(query_delete)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")
