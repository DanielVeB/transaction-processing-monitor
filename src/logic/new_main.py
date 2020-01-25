from src.logic.coordinator import Coordinator

coordinator = Coordinator()
web = coordinator.add_repository(WebSerivce())
web.insert()
web.update()
web.remove()

web2 = coordinator.add_repository(WebSerivce())
web2.insert()
web2.update()
web2.remove()

coordinator.execute_actions()
coordinator.commit()
