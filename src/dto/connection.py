from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.dto import connection_config


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = connection_config.DEFAULT_TYPE + connection_config.URI
# app.config['SQLALCHEMY_BINDS'] = {
#     "posgres": connection_config.OPTIONAL_TYPES['postgres'] + connection_config.URI,
#     "oracle": connection_config.OPTIONAL_TYPES['oracle'] + connection_config.URI
# }
#
# db = SQLAlchemy(app)


class Connection:
    @staticmethod
    def create_connection(connection):
        app.config['SQLALCHEMY_DATABASE_URI'] = connection
        return SQLAlchemy(app)


# class Test_MySQL(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return '<Test %r>' % self.value
#
# class Test_PostgreSQL(db.Model):
#     __bind_key__ = 'postgres'
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return '<Test %r>' % self.value
#
# class Test_Oracle(db.Model):
#     __bind_key__ = 'oracle'
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return '<Test %r>' % self.value
