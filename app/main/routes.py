# Импорты Flask
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

# Импорты проекта
from app import db
from app.models import View, Article
from app.forms import ViewForm, EditArticleForm  # Добавили импорт новой формы

# 🔹 Создание Blueprint для маршрутов
main = Blueprint('main', __name__)

# --- Маршруты работы с Видами изделий ---

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

        # Если нет — создаём новый Вид с названием и описанием
        new_view = View(
            name=form.name.data,
            description=form.description.data
        )
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
        flash('Вид успешно обновлён!', 'success')
        return redirect(url_for('main.index'))

    # Отобразить форму редактирования
    return render_template('edit_view.html', view=view)


# --- Маршруты работы с Артикулами ---

# 🔹 Маршрут для генерации нового Артикула
@main.route('/generator', methods=['POST'])
def generator():
    article_code = request.form.get('article_code')
    description = request.form.get('article_description')

    if not article_code:
        flash('Ошибка: Код артикула пустой.', 'danger')
        return redirect(url_for('main.index'))

    existing = Article.query.filter_by(code=article_code).first()
    if existing:
        flash('Такой артикул уже существует!', 'warning')
    else:
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

# 🔹 Маршрут для получения следующего доступного префикса
@main.route('/get_prefix', methods=['POST'])
def get_prefix():
    partial_code = request.json.get('partial_code')
    if not partial_code or not isinstance(partial_code, str):
        return jsonify({'error': 'Invalid partial_code'}), 400
    matches = Article.query.filter(Article.code.like(f"{partial_code}%")).all()
    existing_prefixes = [int(a.code.split('-')[-1]) for a in matches if a.code.split('-')[-1].isdigit()]
    next_prefix = max(existing_prefixes, default=0) + 1
    return jsonify({'prefix': next_prefix})

# --- НОВОЕ: Маршруты для просмотра и редактирования Артикулов ---

# 🔹 Маршрут для просмотра одного артикула
@main.route('/view_article/<int:article_id>')
def view_article(article_id):
    """
    Страница просмотра одного артикула по его ID
    """
    article = Article.query.get_or_404(article_id)

    # Попытка найти вид изделия по первой букве кода артикула
    view = None
    if article.code:
        first_letter = article.code[0]
        view = View.query.filter(View.name.startswith(first_letter)).first()

    return render_template('view_article.html', article=article, view=view)


# 🔹 Маршрут для редактирования артикула
@main.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    """
    Страница редактирования артикула и его связанного Вида
    """
    article = Article.query.get_or_404(article_id)
    form = EditArticleForm(obj=article)

    # Попытка найти вид изделия по первой букве кода артикула
    view = None
    if article.code:
        first_letter = article.code[0]
        view = View.query.filter(View.name.startswith(first_letter)).first()

    if form.validate_on_submit():
        # Обновляем описание артикула
        article.description = form.description.data

        # Если пользователь передал новые данные для Вида изделия
        if view:
            view.name = request.form.get('view_name') or view.name
            view.description = request.form.get('view_description') or view.description

        db.session.commit()
        flash('Артикул и вид изделия успешно обновлены!', 'success')
        return redirect(url_for('main.view_article', article_id=article.id))

    return render_template('edit_article.html', form=form, article=article, view=view)

# 🔹 Маршрут для удаления Вида изделия
@main.route('/delete_view/<int:view_id>', methods=['POST'])
def delete_view(view_id):
    view = View.query.get_or_404(view_id)

    # Проверка: есть ли артикулы, связанные с этим видом
    linked_articles = Article.query.filter(Article.code.startswith(view.name)).all()

    if linked_articles:
        flash('Невозможно удалить: существуют артикулы, связанные с этим видом.', 'danger')
        return redirect(url_for('main.index'))

    db.session.delete(view)
    db.session.commit()
    flash('Вид успешно удалён!', 'success')
    return redirect(url_for('main.index'))

# 🔹 Маршрут для отображения всех Видов изделий
@main.route('/views')
def list_views():
    views = View.query.order_by(View.name).all()
    return render_template('list_views.html', views=views)

