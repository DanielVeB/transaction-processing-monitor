from src.entity.request import WebServiceData
from src.logic.coordinator import Coordinator

coordinator = Coordinator()

webservice_data_first = WebServiceData("localhost", "8080", ["/", "/", "/"])
webservice_data_second = WebServiceData("localhost", "8081", ["/", "/", "/"])
webservice_first = coordinator.add_service(webservice_data_first)
webservice_second = coordinator.add_service(webservice_data_second)

# How about implementing builder for WebServiceData and converting it to Coordinator._WebService?

webservice_first.add()
webservice_first.remove()
webservice_first.update()

webservice_second.add()
webservice_second.remove()
webservice_second.update()

coordinator.execute_transaction()
coordinator.commit()
