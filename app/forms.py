# app/forms.py

# 🔹 Импорт базового класса FlaskForm
from flask_wtf import FlaskForm

# 🔹 Импорт полей формы
from wtforms import StringField, SubmitField, TextAreaField

# 🔹 Импорт валидаторов
from wtforms.validators import DataRequired

# 🔹 Форма для добавления нового Вида изделия
class ViewForm(FlaskForm):
    name = StringField(
        label='Название вида',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )
    submit = SubmitField('Добавить')

# 🔹 Форма для редактирования Артикула
class EditArticleForm(FlaskForm):
    description = TextAreaField(
        label='Описание артикула',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )
    submit = SubmitField('Сохранить изменения')
