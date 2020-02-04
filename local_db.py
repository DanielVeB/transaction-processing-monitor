# Example
from flask import Flask

from src.library.database_config import DatabaseService

app = Flask(__name__)
URL = "mysql://admin:lukasz@localhost:3306/test"
dbs = DatabaseService(app, URL)
repo = dbs.create_repository()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
