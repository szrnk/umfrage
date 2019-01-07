from behave import *
from django.contrib.auth.models import User

use_step_matcher("re")


@given("I am not authenticated")
def step_impl(context):
    pass


@when("I access the page")
def step_impl(context):
    context.response = context.test.client.get("/")

@then("Status code is (?P<status>\d+)")
def step_impl(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} != {1}".format(code, status)
# TODO: Check this escape sequence.

@given("I am authenticated")
def step_impl(context):
    user = User.objects.create_superuser("jane", "jane@example.org", "123")
    context.test.client.force_login(user)
