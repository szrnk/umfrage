from behave import *

from correspondents.models import Hospital, Department
from features.steps.utils import HospitalFactory
from selenium.webdriver.support.ui import Select


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


@then("I am returned to the hospitals list")
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


@given('that a hospital "{name}" is defined in the system')
def step_impl(context, name):
    """
    :type context: behave.runner.Context
    :param name:
    """
    HospitalFactory(name=name)


@step("I select add-department")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    br = context.browser
    br.get(context.base_url + '/admin/correspondents/department/add/')

    # Checks for Cross-Site Request Forgery protection input
    assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()


@step('I submit the add-department form for "{department_name}" to hospital "{hospital_name}"')
def step_impl(context, department_name, hospital_name):
    """
    :type context: behave.runner.Context
    :param department_name:
    :param hospital_name:
    """

    br = context.browser

    # https://sqa.stackexchange.com/questions/1355/what-is-the-correct-way-to-select-an-option-using-seleniums-python-webdriver
    select = Select(br.find_element_by_id('id_hospital'))
    text_options = [o.text for o in select.options]
    assert hospital_name in text_options
    select.select_by_visible_text(hospital_name)

    br.find_element_by_name('name').send_keys(department_name)
    br.find_element_by_name('address').send_keys('Am Rinzler 2')
    br.find_element_by_name('city').send_keys('Lizelstetten')
    br.find_element_by_name('state_province').send_keys('Schaffhausen')
    br.find_element_by_name('country').send_keys('Schweiz')
    br.find_element_by_name('website').send_keys('sun.com')
    br.find_element_by_name('contact_name').send_keys('A. Einstein')
    br.find_element_by_name('contact_email').send_keys('person@example.com')
    br.find_element_by_name("_save").click()


@then("I am returned to the department list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    assert br.current_url.endswith('/correspondents/department/')


@step("no departments exist")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert not Department.objects.all()


@step("I see one department row")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    rows = br.find_elements_by_xpath("//table[@id='result_list']/tbody/tr")
    assert len(rows) == 1


@step('the name of the department is "{name}"')
def step_impl(context, name):
    """
    :type context: behave.runner.Context
    :param name:
    """

    br = context.browser
    name_saved = br.find_element_by_xpath("//table[@id='result_list']/tbody/tr/th")
    assert name_saved.text == name
