# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ViewForm(FlaskForm):
    name = StringField('Название вида', validators=[DataRequired()])
    description = TextAreaField('Описание')  # это важно
    submit = SubmitField('СОХРАНИТЬ ВИД')