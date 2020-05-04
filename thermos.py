from logging import DEBUG
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel(DEBUG)

bookmarks = []


def store_bookmarks(url):
    bookmarks.append(dict(
        url=url,
        user="Dave",
        date=datetime.utcnow()
    ))


@app.route('/')
# @app.route('/index')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form["url"]
        store_bookmarks(url)
        app.logger.debug('Stored URL: ' + url)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


if __name__ == '__main__':
    app.run()
