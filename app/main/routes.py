

# Импорты проекта
from app import db
from app.models import View, Category, Model, Article, Color
from app.forms import ViewForm, CategoryForm, ModelForm, EditArticleForm, ColorForm
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session



# 🔹 Создание Blueprint
main = Blueprint('main', __name__)


# --- ВИДЫ ---

@main.route('/add_view', methods=['GET', 'POST'])
def add_view():
    form = ViewForm()
    if form.validate_on_submit():
        existing_view = View.query.filter_by(name=form.name.data).first()
        if existing_view:
            flash('Такой вид уже существует!', 'warning')
            return redirect(url_for('main.index'))

        new_view = View(name=form.name.data, description=form.description.data)
        db.session.add(new_view)
        db.session.commit()
        flash('Вид успешно добавлен!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_view.html', form=form)


@main.route('/views')
def list_views():
    views = View.query.order_by(View.name).all()
    return render_template('list_views.html', views=views)


@main.route('/delete_view/<int:view_id>', methods=['POST'])
def delete_view(view_id):
    view = View.query.get_or_404(view_id)
    linked_articles = Article.query.filter(Article.code.startswith(view.name)).all()
    if linked_articles:
        flash('Невозможно удалить: существуют артикулы, связанные с этим видом.', 'danger')
        return redirect(url_for('main.index'))
    db.session.delete(view)
    db.session.commit()
    flash('Вид успешно удалён!', 'success')
    return redirect(url_for('main.index'))


# --- КАТЕГОРИИ ---

@main.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    form.view.choices = [(v.id, v.name) for v in View.query.order_by(View.name).all()]

    if form.validate_on_submit():
        existing = Category.query.filter_by(name=form.name.data, view_id=form.view.data).first()
        if existing:
            flash('Такая категория уже существует в этом виде!', 'warning')
        else:
            category = Category(
                name=form.name.data,
                description=form.description.data,
                view_id=form.view.data
            )
            db.session.add(category)
            db.session.commit()
            flash('Категория успешно добавлена!', 'success')
            return redirect(url_for('main.index'))

    return render_template('add_category.html', form=form)


@main.route('/api/categories/<int:view_id>')
def get_categories(view_id):
    categories = Category.query.filter_by(view_id=view_id).order_by(Category.name).all()
    data = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(data)

@main.route('/api/models/<int:view_id>/<int:category_id>')
def get_models(view_id, category_id):
    """
    Возвращает список моделей для выбранного вида и категории
    в формате JSON: [{'code': '12', 'description': 'дверь стеклянная'}, ...]
    """
    from app.models import Model

    models = Model.query.filter_by(view_id=view_id, category_id=category_id).order_by(Model.code).all()
    data = [{'code': m.code, 'description': m.description or ''} for m in models]
    return jsonify(data)



# --- МОДЕЛИ ---

@main.route('/add_model', methods=['GET', 'POST'])
def add_model():
    form = ModelForm()
    views = View.query.order_by(View.name).all()
    form.view.choices = [(v.id, v.name) for v in views]

    # Найди и удали или закомментируй это:
    # if form.view.data:
    #     form.category.choices = ...
    # else:
    #     form.category.choices = []

    # Вместо этого — просто:
    form.category.choices = []
    # Очищаем список категорий — он будет заполняться на клиенте (JavaScript)

    if form.validate_on_submit():
        model = Model(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data,
            view_id=form.view.data,
            category_id=form.category.data
        )
        db.session.add(model)
        db.session.commit()
        flash("Модель успешно добавлена!", "success")
        return redirect(url_for("main.index"))

    return render_template("add_model.html", form=form)

# --- ДОБАВЛЕНИЕ ЦВЕТА ---
@main.route('/add_color', methods=['GET', 'POST'])
def add_color():
    form = ColorForm()

    if form.validate_on_submit():
        existing_by_code = Color.query.filter_by(code=form.code.data).first()
        existing_by_name = Color.query.filter_by(name=form.name.data).first()

        if existing_by_code or existing_by_name:
            flash("Такой цвет уже существует!", "warning")
        else:
            new_color = Color(
                code=form.code.data.zfill(2),  # Преобразуем в формат '01'
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(new_color)
            db.session.commit()
            flash("Цвет успешно добавлен!", "success")
            return redirect(url_for("main.index"))

    return render_template("add_color.html", form=form)



# --- ГЛАВНАЯ (ГЕНЕРАТОР) ---
@main.route('/', methods=['GET', 'POST'])
def index():
    views = View.query.order_by(View.name).all()
    view_id = request.form.get('view', type=int)
    category_id = request.form.get('category', type=int)
    model_code = request.form.get('model')
    level = request.form.get('level') or "4"

    # Категории по выбранному виду
    if view_id:
        categories = Category.query.filter_by(view_id=view_id).order_by(Category.name).all()

        # Если выбрана и категория — фильтруем точнее
        if category_id:
            models = Model.query.filter_by(view_id=view_id, category_id=category_id).order_by(Model.code).all()
        else:
            # Если категория не выбрана — берём все модели этого вида
            models = Model.query.filter_by(view_id=view_id).order_by(Model.code).all()
    else:
        categories = []
        models = []

    colors = Color.query.order_by(Color.code).all()
    selected_components = session.get('selected_components', [])
    selected_details = session.get('selected_details', [])

    return render_template(
        'index.html',
        views=views,
        categories=categories,
        models=models,
        colors=colors,
        selected_view_id=view_id,
        selected_category_id=category_id,
        selected_model_code=model_code,
        selected_level=level,  # 👈 обязательно для отображения в <select>
        selected_components_count=str(len(selected_components)).zfill(2),
        selected_details_count=str(len(selected_details)).zfill(2)
    )


# --- ГЕНЕРАЦИЯ АРТИКУЛА ---

@main.route('/generator', methods=['POST'])
def generator():
    from flask import session

    # 🔹 Получение значений из формы
    view_id = request.form.get('view')
    category_name = request.form.get('category')
    level = request.form.get('level') or "0"
    is_manual_weight = level == "4"
    model_code = request.form.get('model')
    model_block = model_code if model_code and model_code.isdigit() else '00'
    color = request.form.get('color') or "00"
    blocks = request.form.get('blocks') or "00"
    details = request.form.get('details') or "00"
    prefix = request.form.get('prefix') or "0"
    description = request.form.get('article_description') or ""

    # 🔹 Подготовка расчёта веса и списка дочерних артикулов
    used_articles = []
    total_weight_real = 0.0

    if is_manual_weight:
        # Ручной ввод веса для level = 4
        weight_input = request.form.get('weight')
        try:
            weight_real = float(weight_input)  # точный вес, с 3 знаками позже
            weight_code = round(weight_real, 1)  # округлённый вес (пример: 60.0)
            weight_str = "{:05.1f}".format(weight_code).replace(".", "")  # '060'

        except:
            flash('Ошибка: вес указан некорректно.', 'danger')
            return redirect(url_for('main.index'))
    else:
        # Автоматический расчёт на основе session
        selected_components = session.get('selected_components', [])
        selected_details = session.get('selected_details', [])
        blocks = str(len(selected_components)).zfill(2)
        details = str(len(selected_details)).zfill(2)

        if selected_components:
            components = Article.query.filter(Article.id.in_(selected_components)).all()
            for a in components:
                total_weight_real += a.weight_real
                used_articles.append(a.code)

        if selected_details:
            details_list = Article.query.filter(Article.id.in_(selected_details)).all()
            for a in details_list:
                total_weight_real += a.weight_real
                used_articles.append(a.code)

        weight_real = round(total_weight_real, 3)  # точный вес (3 знака)
        weight_code = round(weight_real, 1)  # округлённый вес (1 знак)
        weight_str = "{:05.1f}".format(weight_code).replace(".", "")  # '060'

    # 🔹 Символ вида
    views = View.query.order_by(View.name).all()
    view_symbol = "X"
    categories = []

    if view_id and view_id.isdigit():
        view = View.query.get(int(view_id))
        if view:
            view_symbol = view.name[0].upper()
            categories = Category.query.filter_by(view_id=view.id).order_by(Category.name).all()
    else:
        view_id = None

    category_code = category_name[:2].upper() if category_name else "XX"

    # 🔹 Финальный код артикула
    article_code = f"{view_symbol}{category_code}{level}-{model_block}{color}{weight_str}-{blocks}{details}-{prefix}"

    if not article_code:
        flash('Ошибка: Код артикула пустой.', 'danger')
        return render_template('index.html',
                               views=views,
                               categories=categories,
                               selected_view_id=view_id,
                               selected_category_name=category_name)

    existing = Article.query.filter_by(code=article_code).first()
    if existing:
        flash('Такой артикул уже существует!', 'warning')
        return render_template('index.html',
                               views=views,
                               categories=categories,
                               selected_view_id=view_id,
                               selected_category_name=category_name)

    # 🔹 Вставка компонентов в описание
    if used_articles:
        description += f"\nКомпоненты: {', '.join(used_articles)}"

    # 🔹 Сохранение в базу с level
    new_article = Article(
        code=article_code,
        description=description,
        weight_real=weight_real,
        weight_code=weight_code,
        level=level
    )

    db.session.add(new_article)
    db.session.commit()

    # 🔹 Очистка выбранных компонентов
    # Очищаем session только при генерации детали (уровень 4)
    if level == "4":
        session.pop('selected_components', None)
        session.pop('selected_details', None)

    flash(f'Артикул {article_code} успешно создан.', 'success')
    return redirect(url_for('main.list_articles'))

# --- ПРОСМОТР И РЕДАКТИРОВАНИЕ ---

@main.route('/articles')
def list_articles():
    search_query = request.args.get('search', '')

    query = Article.query

    if search_query:
        query = query.filter(
            Article.code.ilike(f"%{search_query}%") |
            Article.description.ilike(f"%{search_query}%")
        )

    articles = query.order_by(Article.id.desc()).all()
    return render_template('list_articles.html', articles=articles)



@main.route('/view_article/<int:article_id>')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    view = None
    if article.code:
        first_letter = article.code[0]
        view = View.query.filter(View.name.startswith(first_letter)).first()
    return render_template('view_article.html', article=article, view=view)


@main.route('/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = EditArticleForm(obj=article)
    view = None
    if article.code:
        first_letter = article.code[0]
        view = View.query.filter(View.name.startswith(first_letter)).first()

    if form.validate_on_submit():
        article.description = form.description.data
        if view:
            view.name = request.form.get('view_name') or view.name
            view.description = request.form.get('view_description') or view.description
        db.session.commit()
        flash('Артикул и вид изделия успешно обновлены!', 'success')
        return redirect(url_for('main.view_article', article_id=article.id))

    return render_template('edit_article.html', form=form, article=article, view=view)


# --- ПРЕФИКС АВТОИНКРЕМЕНТ ---

@main.route('/get_prefix', methods=['POST'])
def get_prefix():
    partial_code = request.json.get('partial_code')
    if not partial_code or not isinstance(partial_code, str):
        return jsonify({'error': 'Invalid partial_code'}), 400
    matches = Article.query.filter(Article.code.like(f"{partial_code}%")).all()
    existing_prefixes = [int(a.code.split('-')[-1]) for a in matches if a.code.split('-')[-1].isdigit()]
    next_prefix = max(existing_prefixes, default=0) + 1
    return jsonify({'prefix': next_prefix})


# --- ВЫБОР КОМПОНЕНТОВ ---
@main.route('/select_components', methods=['GET', 'POST'])
def select_components():
    # Отображаем все артикулы уровня 2 и 3
    articles = Article.query.filter(Article.level.in_(["2", "3"])).order_by(Article.code).all()

    if request.method == 'POST':
        # Сохраняем выбранные ID в session
        selected_ids = request.form.getlist('component_ids')
        session['selected_components'] = selected_ids
        flash(f"Выбрано компонентов: {len(selected_ids)}", 'success')
        return redirect(url_for('main.index'))

    return render_template('select_components.html', articles=articles)


# --- ВЫБОР ДЕТАЛЕЙ ---
@main.route('/select_details', methods=['GET', 'POST'])
def select_details():
    # Отображаем все артикулы уровня 4
    articles = Article.query.filter_by(level="4").order_by(Article.code).all()

    if request.method == 'POST':
        selected_ids = request.form.getlist('detail_ids')
        session['selected_details'] = selected_ids
        flash(f"Выбрано деталей: {len(selected_ids)}", 'success')
        return redirect(url_for('main.index'))

    return render_template('select_details.html', articles=articles)
