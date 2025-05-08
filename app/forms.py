# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ViewForm(FlaskForm):
    name = StringField('Название вида', validators=[DataRequired()])
    submit = SubmitField('Добавить')