import argparse
import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=False)
    dob = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    address = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.form:
        user = User(
            username=request.form.get("username"),
            email=request.form.get("email"),
            dob=request.form.get("dob"),
            address=request.form.get("address")
        )
        db.session.add(user)
        db.session.commit()
    return render_template("add-user.html")


@app.route("/list-users", methods=["GET"])
def list_users():
    users = User.query.all()
    return render_template("list-users.html", users=users)


def database_setup():
    db.create_all()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start rest api service.")
    parser.add_argument("--setup", action="store_true", help="Setup the database ready for use and exit.")
    args = parser.parse_args()
    if args.setup:
        database_setup()
    else:
        app.run(debug=True)
