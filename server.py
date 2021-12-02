from flask import Flask, request, json

app = Flask(__name__)


@app.route('/stories')
def stories():
    return 'Webhooks with Python'


if __name__ == '__main__':
    app.run(debug=True)
