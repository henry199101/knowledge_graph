from flask import Flask, request
from forms import SearchForm


app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
@app.route('/index')
def hello():
    return 'Hello World!'


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate() and request.method == 'post':
        return 'post page'
    return 'get page'
