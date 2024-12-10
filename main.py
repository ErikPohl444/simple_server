from flask import Flask, request, make_response, render_template
from markupsafe import escape

app = Flask(__name__)


class Poll:
    name = "Erik"
    question = "why??????"

@app.route('/goodbye/<name>')
def hello(name):
    return f"<h1>Goodbye, !!!!!{escape(name)}!</h1>"

@app.route('/index.html')
def index():
    return render_template('index.html', hostname="hostname", poll=poll)


if __name__ == "__main__":
    poll = Poll()
    app.run()