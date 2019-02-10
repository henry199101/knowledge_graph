from flask import Flask, request, render_template, redirect, url_for, flash
from .forms import SearchForm
from .import_data_to_graph_db import DomainModel


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
        entity_name = form.search_content.data
        form.search_content.data = None

        domain_model = DomainModel()
        query_result = domain_model.query(entity_name=entity_name)

        if query_result is None:
            return render_template('search.html', form=form, entity_name=entity_name, query_result=None)

        labels = query_result.labels
        keys = query_result.keys()
        return render_template('search.html', form=form, entity_name=entity_name, query_result=query_result, labels=labels, keys=keys)

    return render_template('search.html', form=form, query_string=None)
