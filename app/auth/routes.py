from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from . import auth
from app.forms import LoginForm
from app.models import User
from app.extensions import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы вошли в систему.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth.login'))
