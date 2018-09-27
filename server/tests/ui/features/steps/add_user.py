from behave import step


@step("I enter {field} {value}")
def enter_field_value(context, field, value):
    pass


@step(u'I am on the add new user form')
def navigate_to_new_user_form(context):
    pass


@step(u'I press the Add button')
def add_user(context):
    pass


@step(u'I see user is added successfully')
def validate_user_added(context):
    pass
