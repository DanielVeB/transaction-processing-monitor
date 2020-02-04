from src.logic.webservices import WebServiceBuilder
from src.logic.coordinator import Coordinator

coordinator = Coordinator()

webservice_first = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("8081") \
    .rollback_endpoint("/") \
    .with_commit_endpoint("/") \
    .with_send_transaction_endpoint("/") \
    .build()

webservice_second = WebServiceBuilder() \
    .with_host("localhost") \
    .with_port("8082") \
    .rollback_endpoint("/") \
    .with_commit_endpoint("/") \
    .with_send_transaction_endpoint("/") \
    .build()

coordinator.add_service(webservice_first)
coordinator.add_service(webservice_second)

webservice_first.add()
webservice_first.remove()
webservice_first.update()

webservice_second.add()
webservice_second.remove()
webservice_second.update()

coordinator.execute_transaction()
coordinator.commit()
