from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread
from time import sleep


import argparse
import asyncio
import os
import requests
import socket

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
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError



AppSession = namedtuple('AppSession', ['app', 'db', 'api'])

request_parser = reqparse.RequestParser()

ADD_FIELDS = ['username', 'email', 'dob', 'address']
GET_FIELDS = ['id'] + ADD_FIELDS

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


@app.route("/")
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())


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
        if not all(data.values()):
            return "Incomplete form data!", 500
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
        except SQLAlchemyIntegrityError as e:
            return str(e.orig), 500


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
    # wait for the server to fully initialize
    # sleep(10)
    # stop_app()


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

