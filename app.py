from flask import Flask, request, render_template, redirect, url_for
from forms import SearchForm


app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        return 'post page'
    return render_template('search.html', form=form)
