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
    .build()

second_webservice = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9030") \
    .build()

coordinator.add_service(first_webservice)
coordinator.add_service(second_webservice)

director.set_builder(insert_builder)
insert_builder \
    .with_table_name("test") \
    .with_values({"idtest": "656", "value": 989})

insert = director.get_query()
delete_builder \
    .with_table_name("test") \
    .with_where("idtest=34512")

director.set_builder(delete_builder)
delete = director.get_query()

update_builder \
    .with_table_name("test") \
    .with_values({"value": 657}) \
    .with_where("idtest=7787")

director.set_builder(update_builder)
update = director.get_query()

first_webservice.add_query(delete)
first_webservice.add_query(insert)
second_webservice.add_query(update)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Handle exception 1")
