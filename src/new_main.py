from src.logic.coordinator import Coordinator
from src.logic.request import QueryBuilder
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()

webservice_first = WebServiceBuilder() \
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

coordinator.add_service(webservice_first)
coordinator.add_service(second_webservice)

first_query = QueryBuilder() \
    .with_method("INSERT") \
    .with_table_name("test") \
    .with_values({"idtest": 3434, "value": 915199}) \
    .build()

second_query = QueryBuilder() \
    .with_method("INSERT") \
    .with_table_name("test") \
    .with_values({"idtest": 6922, "value": 999}) \
    .build()

webservice_first.add_query(first_query)
second_webservice.add_query(second_query)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")

third_query = QueryBuilder() \
    .with_method("DELETE") \
    .with_table_name("test") \
    .with_where("idtest=3434") \
    .build()

fourth_query = QueryBuilder() \
    .with_method("UPDATE") \
    .with_table_name("test") \
    .with_values({"value": 67823}) \
    .with_where("idtest=6789") \
    .build()

webservice_first.add_query(third_query)
second_webservice.add_query(fourth_query)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 2")
