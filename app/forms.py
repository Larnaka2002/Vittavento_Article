# app/forms.py

# 🔹 Импорт базового класса FlaskForm
from flask_wtf import FlaskForm

# 🔹 Импорт полей формы
from wtforms import StringField, SubmitField

# 🔹 Импорт валидаторов
from wtforms.validators import DataRequired

# 🔹 Форма для добавления нового Вида изделия
class ViewForm(FlaskForm):
    # Поле ввода названия вида изделия
    name = StringField(
        label='Название вида',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )

    # Кнопка для отправки формы
    submit = SubmitField('Добавить')
