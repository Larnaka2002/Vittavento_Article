# app/forms.py

# 🔹 Импорт базового класса FlaskForm
from flask_wtf import FlaskForm

# 🔹 Импорт полей формы
from wtforms import StringField, TextAreaField, SelectField, SubmitField

# 🔹 Импорт валидаторов
from wtforms.validators import DataRequired


# 🔹 Форма для добавления нового Вида изделия
class ViewForm(FlaskForm):
    name = StringField(
        label='Название вида',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )

    # Описание вида
    description = TextAreaField(
        label='Описание вида',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )

    submit = SubmitField('Добавить')


class CategoryForm(FlaskForm):
    # Список доступных видов изделия
    view = SelectField('Выберите Вид', coerce=int, validators=[DataRequired()])

    # Название категории
    name = StringField('Название категории', validators=[DataRequired()])

    # Описание категории (опционально)
    description = TextAreaField('Описание категории')

    submit = SubmitField('Добавить категорию')


# 🔹 Форма для редактирования Артикула
class EditArticleForm(FlaskForm):
    description = TextAreaField(
        label='Описание артикула',
        validators=[DataRequired(message="Поле обязательно для заполнения")]
    )
    submit = SubmitField('Сохранить изменения')

from flask_wtf import FlaskForm

# Простая форма фильтрации вида и категории
class FilterForm(FlaskForm):
    pass  # пока пустая, нужна только для {{ form.hidden_tag() }}
