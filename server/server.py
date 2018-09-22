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


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    return render_template("home.html")


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
