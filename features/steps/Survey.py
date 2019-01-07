from behave import *

from surveys.models import Survey
from core.users.tests.factories import AdminFactory
from django.conf import settings


use_step_matcher("parse")


@given("there are as yet no surveys")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert not Survey.objects.all()


@step("I am logged in as admin")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    u = AdminFactory(username='admin', email='admin@example.com')
    u.set_password('adm1n')
    u.save()

    br = context.browser
    br.get(context.base_url + '/accounts/login/')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    # Fill login form and submit it (valid version)
    br.find_element_by_name('login').send_keys('admin')
    br.find_element_by_name('password').send_keys('adm1n')
    br.find_element_by_class_name('primaryAction').click()

    # did we make it?
    assert br.current_url.endswith('/accounts/confirm-email/')

    br.get(context.base_url + '/users/admin/')
    br.get(context.base_url + '/users/admin/')

    # from django.contrib.sessions.backends.db import SessionStore
    # from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
    #
    # session = SessionStore()
    # session[SESSION_KEY] = u.pk  # 1
    # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    # session.save()

    pass


@when("I login to admin ui")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    br = context.browser
    br.get(context.base_url + '/admin/login/')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    # Fill login form and submit it (valid version)
    br.find_element_by_name('username').send_keys('admin')
    br.find_element_by_name('password').send_keys('adm1n')
    br.find_element_by_xpath("//input[@type='submit']").click()

    print(br.current_url)
    pass


@when("I select add-survey")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    br = context.browser
    br.get(context.base_url + '/admin/surveys/survey/add/')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()


@step('I submit the add-survey form for "{title}"')
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    br.find_element_by_name('name').send_keys(title)
    br.find_element_by_name("_save").click()


@then("I am returned to the surveys page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    assert br.current_url.endswith('/surveys/survey/')


@step("I see one survey row")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    rows = br.find_elements_by_xpath("//table[@id='result_list']/tbody/tr")
    assert len(rows) == 1


@step('The title of the survey is "{title}"')
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :param title:
    """
    br = context.browser
    title_saved = br.find_element_by_xpath("//table[@id='result_list']/tbody/tr/th")
    assert title_saved.text == title

