from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = "localhost"
PORT = ":3306"
DATABASE_NAME = "test"
USERNAME = "root"
PASSWORD = "root"
MYSQL_CONNECTION = "mysql://" + USERNAME + ":" + PASSWORD + "@" + DATABASE_URI + PORT + "/" + DATABASE_NAME

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONNECTION
db = SQLAlchemy(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Test %r>' % self.value

