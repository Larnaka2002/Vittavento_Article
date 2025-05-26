# app/admin.py

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from app.extensions import db
from app.models import View, Category, Article, User, Color, Model



# 🔐 Защищённая админ-панель — доступ только авторизованным
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated  # Можно добавить проверку роли

    def inaccessible_callback(self, name, **kwargs):
        flash("Требуется вход для доступа к админке.", "warning")
        return redirect(url_for('auth.login'))


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


# Создание объекта админки
admin = Admin(name='Vittavento Admin', template_mode='bootstrap4', index_view=SecureAdminIndexView())

# Добавляем модели
def init_admin(app):
    admin.init_app(app)
    admin.add_view(SecureModelView(View, db.session, name="Виды"))
    admin.add_view(SecureModelView(Category, db.session, name="Категории"))
    admin.add_view(SecureModelView(Model, db.session, name="Модели"))
    admin.add_view(SecureModelView(Color, db.session, name="Цвета"))
    admin.add_view(SecureModelView(Article, db.session, name="Артикулы"))
    admin.add_view(SecureModelView(User, db.session, name="Пользователи"))

