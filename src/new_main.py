from src.logic.coordinator import Coordinator
from src.logic.request import Query
from src.logic.webservices import WebServiceBuilder

coordinator = Coordinator()

webservice_first = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("9019") \
    .rollback_endpoint("/rollback") \
    .with_commit_endpoint("/commit") \
    .with_send_transaction_endpoint("/execute") \
    .build()

coordinator.add_service(webservice_first)

query1 = Query("INSERT", "test", {"id": 60, "value": 60})
webservice_first.add_query(query1)
coordinator.execute_transaction()
coordinator.commit()
