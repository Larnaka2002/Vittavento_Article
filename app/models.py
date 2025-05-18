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
