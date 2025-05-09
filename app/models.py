from app import db

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<View {self.name}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), nullable=False, unique=True)  # Артикул
    description = db.Column(db.String(256))  # Краткое описание

    def __repr__(self):
        return f'<Article {self.code}>'