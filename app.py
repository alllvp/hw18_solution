# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение


from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.models import Genre, Movie, Director
from setup_db import db
from views.movies.movies import movies_ns
from views.directors.directors import directors_ns
from views.genres.genres import genres_ns


# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    create_data(app, db)


# функция
def create_data(app, db):
    with app.app_context():
        db.create_all()

        # создать несколько сущностей чтобы добавить их в БД
        genre111 = Genre(name="New111")
        genre112 = Genre(name="New112")
        genre113 = Genre(name="New113")
        director111 = Director(name="Ivan")
        director112 = Director(name="Fedor")
        director113 = Director(name="Olesya")
        movie111 = Movie(title="Ivan's life", description="bla bla", trailer="https://youtube.com", year=2022, rating=10.0, genre_id=111, director_id=111)
        movie112 = Movie(title="Fedor's life", description="bla bla", trailer="https://youtube.com", year=2022, rating=10.0, genre_id=112, director_id=112)
        movie113 = Movie(title="Olesya's life", description="bla bla", trailer="https://youtube.com", year=2022, rating=10.0, genre_id=112, director_id=112)

        with db.session.begin():
            db.session.add_all([genre111, genre112, genre113, director111, director112, director113, movie111, movie112, movie113])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
