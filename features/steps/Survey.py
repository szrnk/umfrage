from behave import *
from django.contrib.sessions.models import Session
from django.core import mail

from core.users.tests.factories import AdminFactory
from correspondents.models import Hospital, Department
from correspondents.tests.factories import basic_hospital_structure
from surveys.models import Survey, Invitation
from surveys.tests.factories import tight_survey_structure

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


@when("I select add-survey")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    br = context.browser
    br.get(context.base_url + '/admin/surveys/survey/add/')


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


@given('there is a tight_survey called "{surveyname}"')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    ss = Survey.objects.filter(name=surveyname)
    if not ss:
        tight_survey_structure(surveyname=surveyname)
    ss = Survey.objects.filter(name=surveyname)
    assert ss


@step('a typical_hospital exists called "{hospital_name}" with department "{department_name}"')
def step_impl(context, hospital_name, department_name):
    """
    :type context: behave.runner.Context
    """
    hh = Hospital.objects.filter(name=hospital_name)
    if not hh:
        basic_hospital_structure(hospital_name=hospital_name, department_name=department_name)
    hh = Hospital.objects.filter(name=hospital_name)
    assert hh


@step('an invitation for "{survey_name}" has been extended to "{department_name}" of "{hospital_name}"')
def step_impl(context, survey_name, department_name, hospital_name):
    """
    :type context: behave.runner.Context
    """
    dept = Department.objects.filter(hospital__name=hospital_name, name=department_name).first()
    survey = Survey.objects.filter(name=survey_name).first()
    invites = Invitation.objects.filter(department_id=dept.pk, survey_id=survey.pk)
    if not invites:
        Invitation.objects.create(department=dept, survey=survey)
    invites = Invitation.objects.filter(department_id=dept.pk, survey_id=survey.pk)
    assert len(invites) == 1
    context.invitation = invites.first()


@when("I visit the link from the invitation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    url_with_token = context.invitation.get_url()
    br = context.browser
    br.get(context.base_url + url_with_token)
    pass


@step('I create a user account for "{username}", "{email}", "{password}"')
def step_impl(context, username, email, password):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.get(context.base_url + '/accounts/signup')
    br.find_element_by_name('username').send_keys(username)
    br.find_element_by_name('email').send_keys(email)
    br.find_element_by_name('password1').send_keys(password)
    br.find_element_by_name('password2').send_keys(password)
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert br.current_url.endswith('/accounts/confirm-email/')


@step("I confirm the email address")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    body = mail.outbox[0].body
    confirm_url = body[body.index('http://'):body.index('\n\nThank you from')]
    br = context.browser
    br.get(confirm_url)
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert br.current_url.endswith('/accounts/login/')


@step('I login as "{username}", "{password}"')
def step_impl(context, username, password):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.find_element_by_name('login').send_keys(username)
    br.find_element_by_name('password').send_keys(password)
    br.find_element_by_xpath("//button[@type='submit']").click()
    assert br.current_url.endswith(f'/users/{username}/')


@then("the relevant ids are in my session")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    sess = Session.objects.all().first()
    decoded = sess.get_decoded()
    assert 'invitation_token' in decoded
    assert 'department_id' in decoded
    assert 'survey_id' in decoded


@step('I can see the survey "{surveyname}" in my browser on the current survey page')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.get(context.base_url + '/surveys/current/')
    assert surveyname in br.find_elements_by_tag_name('h2')[0].text


@step('I can see the invitation to "{surveyname}" in my "{username}" profile list of invitations')
def step_impl(context, surveyname, username):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.get(context.base_url + '/surveys/myinvitations/')
    assert surveyname in br.find_elements_by_xpath("//ul[@id='invitations_list']/li")[0].text


@when('the survey "{surveyname}" is visited for the first time')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.get(context.base_url + '/surveys/current/')
    assert surveyname in br.find_elements_by_tag_name('h2')[0].text


# @then('The session has a progress structure for "{surveyname}" and both section and question indices are 0')
# def step_impl(context, surveyname):
#     """
#     :type context: behave.runner.Context
#     """
#     sess = Session.objects.all().first()
#     decoded = sess.get_decoded()
#     # assert 'progress' in decoded
#     # progress = decoded['progress']
#     survey = Survey.objects.filter(name=surveyname).first()
#     assert str(survey.id) in progress
#     # assert progress[str(survey.id)]['question_index'] == 0
#     # assert progress[str(survey.id)]['section_index'] == 0


@step('There is section, question, and option text for each level of "{surveyname}"')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    br.get(context.base_url + '/surveys/current/')
    survey = Survey.objects.filter(name=surveyname).first()
    for section in survey.sections():
        ss = br.find_element_by_id(f'section_{section.id}')
        assert ss.text == section.title
        for idx, question in enumerate(section.questions()):
            labels = ss.parent.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//label")
            question_text = labels[0].text
            assert question_text == question.text
            # for oidx, option in enumerate(question.options()):
            #     option_text = labels[oidx+1].text
            #     assert option_text == option.text


@step('The second question of "{surveyname}" is multichoice')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    survey = Survey.objects.filter(name=surveyname).first()
    section = survey.section_set.first()

    question = section.question_set.order_by('order').all()[0]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 4

    question = section.question_set.all()[1]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 4
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 0


@step('The third question of "{surveyname}" is select')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    survey = Survey.objects.filter(name=surveyname).first()
    section = survey.section_set.first()

    question = section.question_set.order_by('order').all()[0]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 4

    question = section.question_set.all()[2]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 0
    els = br.find_elements_by_xpath("//div[@id='question_3']//form//option")
    assert len(els) == 4
    assert all([el.text.startswith('text') for el in els])


@step('The fourth question of "{surveyname}" is text')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    survey = Survey.objects.filter(name=surveyname).first()
    section = survey.section_set.first()

    question = section.question_set.order_by('order').all()[0]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 4

    question = section.question_set.all()[3]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//option")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//*[@type='text']")
    assert len(els) == 1


@step('The fifth question of "{surveyname}" is essay')
def step_impl(context, surveyname):
    """
    :type context: behave.runner.Context
    """
    br = context.browser
    survey = Survey.objects.filter(name=surveyname).first()
    section = survey.section_set.first()

    question = section.question_set.all()[4]
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='checkbox']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//input[@type='radio']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//form//option")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//*[@type='text']")
    assert len(els) == 0
    els = br.find_elements_by_xpath(f"//div[@id='question_{question.id}']//textarea")
    assert len(els) == 1


