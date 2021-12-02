import re
from flask import Flask, request, json
import backend
import logging
from multiprocessing import Value

app = Flask(__name__)

LOG_FILEPATH = '/application.log'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
h = logging.handlers.RotatingFileHandler(
    LOG_FILEPATH, 'a', maxBytes=5242880, backupCount=1)
f = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

h.setFormatter(f)
logger.addHandler(h)

request_count = Value('i', 0)


@app.route('/stories')
def stories():
    stories = backend.getStories()
    with request_count.get_lock():
        request_count.value += 1
        out = request_count.value
    logging.info("Request count: {count}".format(count=request_count))

    return stories


if __name__ == '__main__':
    app.run(debug=True)
