import argparse
import os
import requests

from collections import namedtuple
from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask_restful import (
    Api,
    reqparse,
    Resource,
)
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import IntegrityError


AppSession = namedtuple('AppSession', ['app', 'db', 'api'])

request_parser = reqparse.RequestParser()

ADD_FIELDS = ['username', 'email', 'dob', 'address']
GET_FIELDS = ['id'] + ADD_FIELDS

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)


def configure_service(db_path):
    global api
    global app
    global db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    db.init_app(app)
    api.add_resource(AddUser, '/api/add')
    api.add_resource(ListUsers, '/api/list')
    if not os.path.exists(db_path):
        db.create_all(app=app)
    return AppSession(app, db, api)


@app.route("/add-user", methods=["GET"])
def add_user():
    return render_template("add-user.html")


@app.route("/list-users", methods=["GET"])
def list_users():
    return render_template("list-users2.html")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    email = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    dob = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    address = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


class AddUser(Resource):

    def get(self):
        req_args = request_parser.parse_args()
        return {'data': 'hello world!'}, 200

    def post(self):
        data = {field: request.form.get(field) for field in ADD_FIELDS}
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError as e:
            return e.orig, 500

class ListUsers(Resource):

    def get(self):
        req_args = request_parser.parse_args()
        users = User.query.all()
        data = {
            'users': [{field: getattr(u, field) for field in User.__table__.columns.keys()} for u in users]
        }
        return data

    def post(self):
        req_args = request_parser.parse_args()


def get_db_path(db_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)


def start_service(db_path, port=5000):
    configure_service(db_path)
    app.run(debug=True, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start rest api service.")
    parser.add_argument("--db", default="database.db", help="Name of the database to use.")
    parser.add_argument("--port", default="5000", help="Port number to run the service on.")
    args = parser.parse_args()
    start_service(get_db_path(args.db))

