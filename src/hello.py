from flask import Flask
import logging


app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@app.route('/hello')
def hello_index():
    return 'Hello World from Python Flask!'


app.run(host='0.0.0.0', port=8080)
