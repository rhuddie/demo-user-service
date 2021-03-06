import argparse
import os
import re

from collections import namedtuple
from datetime import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask_restful import (
    Api,
    reqparse,
    Resource,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread

ADD_FIELDS = ['username', 'email', 'dob', 'address']
GET_FIELDS = ['id'] + ADD_FIELDS
AppSession = namedtuple('AppSession', ['app', 'db', 'api'])
request_parser = reqparse.RequestParser()

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)

server_thread = None
server_thread_io_loop = None
server_thread_http_server = None


def configure_service(db_path):
    global api
    global app
    global db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    return render_template("list-users.html")


@app.route("/")
def home():
    return render_template("home.html")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    email = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    dob = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    address = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)


class AddUser(Resource):

    @staticmethod
    def post():
        data = {field: request.form.get(field) for field in ADD_FIELDS}
        if not all(data.values()):
            return "Incomplete form data!", 500
        if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", data['email'])):
            return f"Invalid email address: {data['email']}!", 500
        try:
            datetime.strptime(data['dob'], "%d/%m/%Y")
        except ValueError:
            return f"Invalid dob: {data['dob']}! Should by DD/MM/YYYY", 500
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except SQLAlchemyIntegrityError as e:
            return str(e.orig), 500
        return user.id, 200


class ListUsers(Resource):

    @staticmethod
    def get():
        users = User.query.all()
        return {'users': [{k: getattr(u, k) for k in User.__table__.columns.keys()} for u in users]}


def get_db_path(db_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)


def start_service(db_path, port):
    configure_service(db_path)
    start_app(port)


def start_app(port):
    def start():
        global server_thread_http_server
        global server_thread_io_loop
        server_thread_io_loop = IOLoop(make_current=True)
        server_thread_http_server = HTTPServer(WSGIContainer(app))
        server_thread_http_server.listen(port)
        server_thread_io_loop.start()
    global server_thread
    server_thread = Thread(target=start)
    server_thread.start()


def stop_app():
    server_thread_http_server.stop()
    server_thread_io_loop.add_callback(server_thread_io_loop.stop)
    server_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start rest api service.")
    parser.add_argument("--db", default="database.db", help="Name of the database to use.")
    parser.add_argument("--port", default="5000", help="Port number to run the service on.")
    args = parser.parse_args()
    server_port = int(os.getenv('SERVER_PORT', 5000))
    start_service(get_db_path(args.db), server_port)
