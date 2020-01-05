# DB credentials
DATABASE_URI = "localhost"
PORT = ":3306"
DATABASE_NAME = "test"
USERNAME = "root"
PASSWORD = "root"


URI = USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME
DEFAULT_TYPE = "mysql://"
OPTIONAL_TYPES = {
    "postgres": "postgresql://",
    "oracle": "oracle://"
}