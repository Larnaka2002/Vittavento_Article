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
    # Уникальный идентификатор артикула
    id = db.Column(db.Integer, primary_key=True)

    # Код артикула (обязательно уникальный)
    code = db.Column(db.String(64), nullable=False, unique=True)

    # Краткое описание артикула (опционально)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'<Article id={self.id} code={self.code}>'
