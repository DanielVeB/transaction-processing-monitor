from src.logic.coordinator import Coordinator
from src.logic.request import Query
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()

webservice_first = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9035") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

coordinator.add_service(webservice_first)
query1 = Query("DELETE", "test", {}, "idtest=39")
query2 = Query("INSERT", "test", {"idtest": 55, "value": 90})
query3 = Query("UPDATE", "test", {"value": 6666}, "idtest=4")
webservice_first.add_query(query1)
webservice_first.add_query(query2)
webservice_first.add_query(query3)

webservice_second = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9030") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

coordinator.add_service(webservice_second)
query4 = Query("INSERT", "test", {"idtest": 3, "value": 90})
webservice_second.add_query(query4)

try:
    coordinator.execute_transaction()
    coordinator.commit()
except:
    print("Dupa")
