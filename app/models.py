# app/models.py

# 🔹 Импорт SQLAlchemy объекта db
from app import db

# 🔹 Модель "Вид изделия"
class View(db.Model):
    # Уникальный идентификатор вида
    id = db.Column(db.Integer, primary_key=True)

    # Название вида изделия (уникальное)
    name = db.Column(db.String(64), nullable=False, unique=True)

    # Описание вида изделия (необязательное)
    description = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<View id={self.id} name={self.name}>'

# Категория изделия, связанная с определённым видом
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Название категории (например, "GLASS" или "METAL")
    name = db.Column(db.String(50), nullable=False)

    # Описание категории (опционально)
    description = db.Column(db.Text)

    # Связь с видом изделия (обязательна)
    view_id = db.Column(db.Integer, db.ForeignKey('view.id'), nullable=False)

    # Отношение к модели View
    view = db.relationship('View', backref=db.backref('categories', lazy=True))

    # Уникальность категории в рамках одного вида
    __table_args__ = (
        db.UniqueConstraint('view_id', 'name', name='uix_view_category'),
    )


# 🔹 Модель "Артикул изделия"
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))

    # Точный вес (например, 74.637)
    weight_real = db.Column(db.Float(precision=5), nullable=False)

    # Уровень артикула: 1 — сборка, 2–3 — компоненты, 4 — отдельные детали
    level = db.Column(db.String(1), nullable=False, default="0")

    # Округлённый вес (например, 74.6)
    weight_code = db.Column(db.Float(precision=1), nullable=False)

    def __repr__(self):
        return f'<Article id={self.id} code={self.code}>'


# 🔧 Модель изделия — привязана к виду и категории, используется в артикулах (2 цифры: 01, 12 и т.д.)
class Model(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)

    # Название модели (например, "Classic", "Urban")
    name = db.Column(db.String(50), nullable=False)

    # Код модели для артикула (две цифры: "01", "12")
    code = db.Column(db.String(2), nullable=False)

    # Описание модели (необязательно)
    description = db.Column(db.Text)

    # Привязка к виду
    view_id = db.Column(db.Integer, db.ForeignKey('view.id'), nullable=False)
    view = db.relationship('View', backref=db.backref('models', lazy=True))

    # Привязка к категории
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('models', lazy=True))

    # Уникальность: в пределах вида и категории код модели должен быть уникален
    __table_args__ = (
        db.UniqueConstraint('view_id', 'category_id', 'code', name='uix_view_category_model_code'),
    )

    def __repr__(self):
        return f"<Model {self.code} - {self.name}>"

# 🎨 Модель Color — для хранения цветов, используемых в артикулах
class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Двузначный код цвета, отображаемый в артикуле (например, '01', '99')
    code = db.Column(db.String(2), nullable=False, unique=True)

    # Название цвета (например: "Белый матовый")
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Описание (необязательно, можно использовать при отображении)
    description = db.Column(db.Text)


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin / user / manager

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



