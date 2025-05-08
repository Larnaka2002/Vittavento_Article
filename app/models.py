from app import db

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<View {self.name}>'