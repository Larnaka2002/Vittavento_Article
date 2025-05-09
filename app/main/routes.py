from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import View
from app.forms import ViewForm
from flask import render_template, redirect, url_for, flash, request
from flask import request, redirect, url_for, flash, render_template
from app.models import Article
from flask import request, jsonify

main = Blueprint('main', __name__)  # создаём blueprint с именем 'main'

@main.route('/add_view', methods=['GET', 'POST'])
def add_view():
    form = ViewForm()
    if form.validate_on_submit():
        # Проверка: есть ли уже такой вид
        existing_view = View.query.filter_by(name=form.name.data).first()
        if existing_view:
            flash('Такой вид уже существует!', 'warning')
            return redirect(url_for('main.index'))

        new_view = View(name=form.name.data)
        db.session.add(new_view)
        db.session.commit()
        flash('Вид успешно добавлен!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_view.html', form=form)

@main.route('/')
def index():
    views = View.query.order_by(View.name).all()
    return render_template('index.html', views=views)

@main.route('/edit_view/<int:view_id>', methods=['GET', 'POST'])
def edit_view(view_id):
    view = View.query.get_or_404(view_id)

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_description = request.form.get('description')

        view.name = new_name
        view.description = new_description

        db.session.commit()
        flash('Вид успешно обновлён', 'success')
        return redirect(url_for('main.index'))

    return render_template('edit_view.html', view=view)

@main.route('/generator', methods=['POST'])
def generator():
    article_code = request.form.get('article_code')
    description = request.form.get('article_description')

    # Проверка: есть ли уже такой артикул
    existing = Article.query.filter_by(code=article_code).first()
    if existing:
        flash('Такой артикул уже существует!', 'warning')
    else:
        new_article = Article(code=article_code, description=description)
        db.session.add(new_article)
        db.session.commit()
        flash('Артикул успешно создан.', 'success')

    return redirect(url_for('main.list_articles'))

@main.route('/articles')
def list_articles():
    # Импортируй модель Article, если ещё не подключена
    from app.models import Article

    # Получаем все артикулы
    articles = Article.query.order_by(Article.id.desc()).all()

    return render_template('list_articles.html', articles=articles)

@main.route('/get_prefix', methods=['POST'])
def get_prefix():
    from app.models import Article

    partial_code = request.json.get('partial_code')
    if not partial_code:
        return jsonify({'error': 'Missing partial_code'}), 400

    # Находим все совпадающие артикулы
    matches = Article.query.filter(Article.code.like(f"{partial_code}%")).all()
    existing_prefixes = [int(a.code.split('-')[-1]) for a in matches]

    next_prefix = max(existing_prefixes, default=0) + 1

    return jsonify({'prefix': next_prefix})

