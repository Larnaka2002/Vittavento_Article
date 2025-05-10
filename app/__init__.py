# app/__init__.py

# 🔹 Импорт сторонних библиотек
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 🔹 Инициализация объектов базы данных и миграций
db = SQLAlchemy()
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

    # Возвращение настроенного приложения
    return app
