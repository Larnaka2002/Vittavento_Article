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
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас нет прав для доступа к этому разделу.", "warning")
        return redirect(url_for('auth.login'))

# ✅ Для модели Article (оставляем как есть)
class ArticleManagerView(ModelView):
    column_filters = ['code', 'description', 'level', 'weight_real', 'weight_code']
    column_searchable_list = ['code', 'description']
    column_sortable_list = ['code', 'level', 'weight_real', 'weight_code']
    column_labels = {
        'code': 'Артикул',
        'description': 'Описание',
        'level': 'Уровень',
        'weight_real': 'Вес (точный)',
        'weight_code': 'Вес (в коде)'
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role in ['admin', 'manager']

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас нет доступа к этому разделу.", "warning")
        return redirect(url_for('auth.login'))

# ✅ Новый — для модели Color
class ColorManagerView(ModelView):
    column_filters = ['name', 'code']
    column_searchable_list = ['name', 'code']
    column_sortable_list = ['name', 'code']
    column_labels = {
        'name': 'Название',
        'code': 'Код'
    }

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role in ['admin', 'manager']

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас нет доступа к этому разделу.", "warning")
        return redirect(url_for('auth.login'))




class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("Доступ запрещён. Войдите как администратор.", "danger")
        return redirect(url_for('auth.login'))


# Создание объекта админки
admin = Admin(name='Vittavento Admin', template_mode='bootstrap4', index_view=SecureAdminIndexView())

# Добавляем модели
def init_admin(app):
    admin.init_app(app)
    admin.add_view(SecureModelView(View, db.session, name="Виды"))
    admin.add_view(SecureModelView(Category, db.session, name="Категории"))
    admin.add_view(SecureModelView(Model, db.session, name="Модели"))
    admin.add_view(ArticleManagerView(Article, db.session, name="Артикулы"))
    admin.add_view(ColorManagerView(Color, db.session, name="Цвета"))  # ✅ здесь было неправильно
    admin.add_view(SecureModelView(User, db.session, name="Пользователи"))


