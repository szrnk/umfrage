from behave import *

from correspondents.models import Hospital
from core.users.tests.factories import AdminFactory
from django.conf import settings


use_step_matcher("parse")


@given("there are as yet no hospitals")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert not Hospital.objects.all()


@when("I select add-hospital")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    br = context.browser
    br.get(context.base_url + '/admin/correspondents/hospital/add/')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()


@step('I submit the add-hospital form for "{title}"')
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    """
    br = context.browser

    br.find_element_by_name('name').send_keys(title)
    br.find_element_by_name('address').send_keys('Am Rinzler 2')
    br.find_element_by_name('city').send_keys('Lizelstetten')
    br.find_element_by_name('state_province').send_keys('Schaffhausen')
    br.find_element_by_name('country').send_keys('Schweiz')
    br.find_element_by_name('website').send_keys('sun.com')
    br.find_element_by_name('email').send_keys('person@example.com')
    br.find_element_by_name("_save").click()


@then("I am returned to the correspondents page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    assert br.current_url.endswith('/correspondents/hospital/')


@step("I see one hospital row")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    rows = br.find_elements_by_xpath("//table[@id='result_list']/tbody/tr")
    assert len(rows) == 1


@step('The title of the hospital is "{title}"')
def step_impl(context, title):
    """
    :type context: behave.runner.Context
    :param title:
    """
    br = context.browser
    title_saved = br.find_element_by_xpath("//table[@id='result_list']/tbody/tr/th")
    assert title_saved.text == title

