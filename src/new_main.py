from src.logic.builder import QueryDirector, InsertQueryBuilder, DeleteQueryBuilder, UpdateQueryBuilder
from src.logic.coordinator import Coordinator
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()
director = QueryDirector()

insert_builder = InsertQueryBuilder()
update_builder = UpdateQueryBuilder()
delete_builder = DeleteQueryBuilder()

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

director.set_builder(insert_builder)
insert_builder.with_table_name("test").with_values({"idtest": "34512", "value": 989})

first_webservice.add_query(director.get_query())
second_webservice.add_query(director.get_query())

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")
