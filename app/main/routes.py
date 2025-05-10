# Импорты Flask
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

# Импорты проекта
from app import db
from app.models import View, Article
from app.forms import ViewForm

# 🔹 Создание Blueprint для маршрутов
main = Blueprint('main', __name__)

# 🔹 Маршрут для добавления нового Вида изделия
@main.route('/add_view', methods=['GET', 'POST'])
def add_view():
    form = ViewForm()
    if form.validate_on_submit():
        # Проверка: существует ли уже такой Вид
        existing_view = View.query.filter_by(name=form.name.data).first()
        if existing_view:
            flash('Такой вид уже существует!', 'warning')
            return redirect(url_for('main.index'))

        # Если нет — создаём новый Вид
        new_view = View(name=form.name.data)
        db.session.add(new_view)
        db.session.commit()
        flash('Вид успешно добавлен!', 'success')
        return redirect(url_for('main.index'))

    # Отобразить форму добавления Вида
    return render_template('add_view.html', form=form)

# 🔹 Главная страница - список всех Видов изделий
@main.route('/')
def index():
    views = View.query.order_by(View.name).all()
    return render_template('index.html', views=views)

# 🔹 Маршрут для редактирования существующего Вида изделия
@main.route('/edit_view/<int:view_id>', methods=['GET', 'POST'])
def edit_view(view_id):
    view = View.query.get_or_404(view_id)

    if request.method == 'POST':
        # Получаем новые данные из формы
        new_name = request.form.get('name')
        new_description = request.form.get('description')

        # Обновляем поля Вида
        view.name = new_name
        view.description = new_description

        # Сохраняем изменения
        db.session.commit()
        flash('Вид успешно обновлён', 'success')
        return redirect(url_for('main.index'))

    # Отобразить форму редактирования
    return render_template('edit_view.html', view=view)

# 🔹 Маршрут для генерации нового Артикула
@main.route('/generator', methods=['POST'])
def generator():
    article_code = request.form.get('article_code')
    description = request.form.get('article_description')

    # Проверка: код артикула не должен быть пустым
    if not article_code:
        flash('Ошибка: Код артикула пустой.', 'danger')
        return redirect(url_for('main.index'))  # ❗ Лучше вернуться на генератор, а не на список

    # Проверка: существует ли уже такой артикул
    existing = Article.query.filter_by(code=article_code).first()
    if existing:
        flash('Такой артикул уже существует!', 'warning')
    else:
        # Создание нового артикула
        new_article = Article(code=article_code, description=description)
        db.session.add(new_article)
        db.session.commit()
        flash('Артикул успешно создан.', 'success')

    return redirect(url_for('main.list_articles'))

# 🔹 Маршрут для отображения всех артикулов
@main.route('/articles')
def list_articles():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('list_articles.html', articles=articles)

# 🔹 Маршрут для получения следующего доступного префикса для артикула
@main.route('/get_prefix', methods=['POST'])
def get_prefix():
    partial_code = request.json.get('partial_code')

    # Проверка: partial_code должен быть валидным
    if not partial_code or not isinstance(partial_code, str):
        return jsonify({'error': 'Invalid partial_code'}), 400

    # Поиск всех артикулов, начинающихся с partial_code
    matches = Article.query.filter(Article.code.like(f"{partial_code}%")).all()

    # Извлекаем существующие префиксы
    existing_prefixes = [int(a.code.split('-')[-1]) for a in matches if a.code.split('-')[-1].isdigit()]

    # Вычисляем следующий доступный префикс
    next_prefix = max(existing_prefixes, default=0) + 1

    return jsonify({'prefix': next_prefix})
