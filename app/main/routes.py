from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import View
from app.forms import ViewForm

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

@main.route('/generator')
def generator():
    return render_template('generator.html')