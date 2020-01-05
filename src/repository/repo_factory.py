from src.repository import repos
from src.dto import connection_config


#
# class RepoFactory:
#     factories = {}
#     def addFactory(id, repoFactory):
#         RepoFactory.factories.put[id] = repoFactory
#     addFactory = staticmethod(addFactory)
#     # A Template Method:
#     def createRepo(id):
#         if not RepoFactory.factories.has_key(id):
#             RepoFactory.factories[id] = \
#               eval(id + '.Factory()')
#         return RepoFactory.factories[id].create()
#     createRepo = staticmethod(createRepo)


class RepoFactory:

    def getRepo(self, repo_type):

        if repo_type == "mysql":
            return repos.TestRepository(connection_config.REPO_TYPES['mysql'] + connection_config.URI)

        elif repo_type == "postgresql":
            return repos.TestRepository(connection_config.REPO_TYPES['postgres'] + connection_config.URI)

        elif repo_type == "oracle":
            return repos.TestRepository(connection_config.REPO_TYPES['oracle'] + connection_config.URI)

        return None

