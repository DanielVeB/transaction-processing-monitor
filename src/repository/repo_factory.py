from src.repository import repos
from src.dto import connection_config

# to factory jakies typowo pythonowe bo oni w sumie to nie maja interfejsow

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
            return repos.TestMySQL(connection_config.MYSQL_URI)

        elif repo_type == "postgresql":
            return repos.TestMySQL(connection_config.POSTGRES_URI)

        elif repo_type == "oracle":
            return repos.TestMySQL(connection_config.ORACLE_URI)

        return None

