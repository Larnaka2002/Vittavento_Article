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
