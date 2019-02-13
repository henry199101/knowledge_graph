from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    search_content  = StringField(validators=[DataRequired()])
    search_button   = SubmitField('Search')
