import backend
import logging
import sys
from multiprocessing import Value
from logging.handlers import RotatingFileHandler
from flask import Flask, request, json

app = Flask(__name__)


logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

request_count = Value('i', 0)


@app.route('/stories')
def stories():
    stories = backend.getStories()
    with request_count.get_lock():
        request_count.value += 1
    app.logger.info("Request count: {count}".format(count=request_count.value))

    return stories


if __name__ == '__main__':
    app.run(debug=True)
