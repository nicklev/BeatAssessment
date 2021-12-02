from flask import Flask, request, json
import backend

app = Flask(__name__)


@app.route('/stories')
def stories():
    stories = backend.getStories()
    return stories


if __name__ == '__main__':
    app.run(debug=True)
