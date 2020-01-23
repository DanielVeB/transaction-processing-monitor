import logging

from flask import Flask, request

from src.entity.request import DP_Transaction, DP_Statement
from src.logic.coordinator import Coordinator

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

coordinator = Coordinator()


class Invalid_ID(Exception):
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.message = message
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def get_values(statement):
    try:
        values_dict = {}
        values = statement['values']
        for value in values:
            key, val = value.split(":")
            values_dict[key] = val
        return values_dict
    except:
        return {}


def get_where(statement):
    try:
        return statement['where']
    except:
        return None


# Transaction
@app.route('/dp/transaction', methods=['GET', 'POST'])
def transaction():
    if request.method == 'POST':
        transactions = []
        content = request.get_json()
        for transaction in content:
            statements = []
            for statement in transaction['statements']:
                statements.append(
                    DP_Statement(
                        method=statement['method'],
                        table_name=statement['table_name'],
                        values=get_values(statement),
                        where=get_where(statement)
                    )
                )
            t = DP_Transaction(
                repository_id=transaction['repository_id'],
                statements=statements
            )
            transactions.append(t)
        coordinator.set_transactions(transactions)
        return "Done"
    else:
        return "TODO"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
