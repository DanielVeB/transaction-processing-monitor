# DB credentials
DATABASE_URI = "localhost"
PORT = ":3306"
DATABASE_NAME = "test"
USERNAME = "root"
PASSWORD = "root"


URI = USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME
REPO_TYPES = {
    "mysql": "mysql://",
    "postgres": "postgresql://",
    "oracle": "oracle://"
}