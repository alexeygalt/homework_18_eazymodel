from flask_restx import Resource, Namespace
from flask import request, abort
from data.models import Movie, movies_schema, movie_schema
from setup_db import db

movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_key = request.args.get("director_id")
        genre_key = request.args.get("genre_id")
        year_key = request.args.get("year_id")
        if director_key:
            result = db.session.query(Movie).filter(Movie.director_id == int(director_key)).all()
        elif genre_key:
            result = db.session.query(Movie).filter(Movie.genre_id == int(genre_key)).all()
        elif genre_key:
            result = db.session.query(Movie).filter(Movie.year == int(year_key)).all()
        else:
            result = db.session.query(Movie).all()

        return movies_schema.dump(result), 200

    def post(self):
        upload_data = request.get_json()
        new_movie = Movie(**upload_data)
        db.session.add(new_movie)
        db.session.commit()
        return "", 201


@movies_ns.route('/<int:mid>')
class MoviesView(Resource):
    def get(self, mid):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            abort(404)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            abort(404)
        upload_date = request.get_json()
        movie.title = upload_date.get('title')
        movie.description = upload_date.get('description')
        movie.trailer = upload_date.get('trailer')
        movie.year = upload_date.get('year')
        movie.rating = upload_date.get('rating')
        db.session.add(movie)
        db.session.commit()
        return "", 201

    def delete(self, mid):
        movie = db.session.query(Movie).get(mid)
        if not movie:
            abort(404)
        db.session.delete(movie)
        db.session.commit()
        return "", 204
