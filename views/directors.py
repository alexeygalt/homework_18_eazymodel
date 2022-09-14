from flask_restx import Resource, Namespace
from flask import abort
from data.models import Director, directors_schema, director_schema
from setup_db import db

directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors)


@directors_ns.route('/<int:did>')
class DirectorsView(Resource):
    def get(self, did):
        director = db.session.query(Director).get(did)
        if not director:
            abort(404)
        return director_schema.dump(director), 200
