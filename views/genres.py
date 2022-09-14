from flask_restx import Resource, Namespace
from flask import request, abort
from data.models import Genre, genres_schema, genre_schema
from setup_db import db

#
genres_ns = Namespace('genres')


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        upload_data = request.get_json()
        new_genre = Genre(**upload_data)
        db.session.add(new_genre)
        db.session.commit()
        return "", 201


@genres_ns.route('/<int:gid>')
class GenresView(Resource):
    def get(self, gid):
        genre = db.session.query(Genre).get(gid)
        if not genre:
            abort(404)
        return genre_schema.dump(genre), 200

