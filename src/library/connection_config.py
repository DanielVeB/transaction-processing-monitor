# DB credentials for test
DATABASE_URI = "localhost"
PORT = ":3306"
DATABASE_NAME = "test"
USERNAME = "root"
PASSWORD = "lukasz"

REPO_TYPES = {
    "mysql": "mysql://",
    "postgres": "postgresql://",
    "oracle": "oracle://"
}

URI = REPO_TYPES["mysql"] + USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME