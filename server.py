from flask import Flask, request, json
import backend
import logging
from multiprocessing import Value
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

LOG_FILEPATH = 'application.log'


# h = logging.handlers.RotatingFileHandler(
#     LOG_FILEPATH, 'a', maxBytes=5242880, backupCount=1)
# h.setLevel(logging.INFO)

# f = logging.Formatter(
#     fmt='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# h.setFormatter(f)
# app.logger.addHandler(h)

logging.basicConfig(filename=LOG_FILEPATH, level=logging.INFO,
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
