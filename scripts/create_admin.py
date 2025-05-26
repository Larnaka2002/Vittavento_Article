import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# scripts/create_admin.py

from app import create_app
from app.extensions import db
from app.models import User

# Инициализируем Flask-приложение
app = create_app()

# Открываем контекст приложения
with app.app_context():
    # Проверяем, существует ли уже пользователь
    existing = User.query.filter_by(email="admin@vittavento.com").first()
    if existing:
        print("⚠️ Пользователь уже существует.")
    else:
        # Создаём пользователя
        user = User(email="admin@vittavento.com")
        user.set_password("123456")  # 👉 можно сменить на более надёжный
        db.session.add(user)
        db.session.commit()
        print("✅ Администратор создан: admin@vittavento.com / 123456")
