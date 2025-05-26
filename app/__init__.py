# app/__init__.py

# 🔹 Импорт сторонних библиотек
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .extensions import db, login_manager
from app.admin import init_admin



# 🔹 Инициализация объектов базы данных и миграций
migrate = Migrate()

# 🔹 Функция создания экземпляра Flask-приложения
def create_app():
    # Создание объекта приложения
    app = Flask(__name__)

    # Конфигурация приложения
    app.config['SECRET_KEY'] = 'secret-key'  # Секретный ключ для сессий и форм (позже лучше через .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Путь к базе данных
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение лишнего трекинга изменений

    # Инициализация базы данных с приложением
    db.init_app(app)

    # Инициализация системы миграций с приложением
    migrate.init_app(app, db)

    # Регистрация маршрутов через Blueprint
    from app.main.routes import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth)

    from app import models  # 📌 Обеспечивает регистрацию всех моделей в контексте миграций

    # 🔹 Настройка менеджера входа
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # 👉 это укажем позже, когда создадим Blueprint 'auth'
    init_admin(app)


    return app

