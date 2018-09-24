import argparse
import os
import requests

from flask import Flask
from flask import render_template
from flask import request
from flask_restful import (
    Api,
    reqparse,
    Resource,
)
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

api = Api(app)

db = SQLAlchemy(app)

request_parser = reqparse.RequestParser()

ADD_FIELDS = ['username', 'email', 'dob', 'address']
GET_FIELDS = ['id'] + ADD_FIELDS


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
        db.session.commit()



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


@app.route("/add-user", methods=["GET"])
def add_user():
    return render_template("add-user.html")


@app.route("/list-users", methods=["GET"])
def list_users():
    return render_template("list-users2.html")


def database_setup():
    db.create_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start rest api service.")
    parser.add_argument("--setup", action="store_true", help="Setup the database ready for use and exit.")
    args = parser.parse_args()
if args.setup:
    database_setup()
else:
    api.add_resource(AddUser, '/add')
    api.add_resource(ListUsers, '/list')
    app.run(debug=True)
