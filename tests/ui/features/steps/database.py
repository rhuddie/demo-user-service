from behave import step

from server.server import (
    User
)


@step("I start with an empty database")
def start_empty_database(context):
    with context.session.app.app_context():
        context.session.db.session.query(User).delete()
        context.session.db.session.commit()
