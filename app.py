from flask import Flask, request, render_template, redirect, url_for, flash
from .forms import SearchForm
from .import_data_to_graph_db import DomainModel


app = Flask(__name__)
app.secret_key = 'secret key'


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('search'))


@app.route('/search/', methods=['GET', 'POST'])
@app.route('/search/<entity_name>', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        #mention = request.args.get('mention')
        entity_name = form.search_content.data

        form.search_content.data = None

        domain_model = DomainModel()
        query_results = domain_model.query(entity_name=entity_name)
        print(query_results.first())

        if len(query_results) == 0:
            return render_template('search_no_result_page.html', form=form, entity_name=entity_name, query_result=None)

        if len(query_results) == 1:
            query_result = query_results.first()
            labels = query_result.labels
            keys = query_result.keys()
            return render_template('search_one_result_page.html', form=form, entity_name=entity_name, query_result=query_result, labels=labels, keys=keys)

        if len(query_results) >= 2:
            return render_template('search_some_results_page.html', form=form, entity_name=entity_name, query_results=query_results)

    return render_template('search_base_page.html', form=form, query_string=None)


from flask import Markup
@app.route('/fakesearch/<mention>')
def fakesearch(mention):
    baiducard = '“383”方案， 是指2013年由国家发展改革委副主任<a>刘鹤</a>担纲领衔撰写的一个改革方案，包含“三位一体改革思路、八个重点改革领域、三个关联性改革组合”的中国新一轮<a>改革</a>路线图。该方案建议将改革分为三个阶段，即2013年至2014年的近期改革、2015年至2017年的中期改革和2018年至2020年的远期改革。'
    #query_results_0_
    mention = request.args.get('mention')
    #response = 'hello, <a href="http://www.baidu.com">%s</a>' % name
    response = 'hello, <a href="{{ url_for('') }}">hihi</a>'
    response = Markup(baiducard)
    return response
    #resp2 = '<a href='http://www.baidu.com'>百度</a>'
    #return render_template('temp.html', response=response)
