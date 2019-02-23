from surveys.models import Answer


def create_survey_output(survey):
    aa = Answer.objects.filter(question__parent_section__survey_id=survey.id).order_by('department').all()
    aa = list(aa)
    for a in aa:
        print(a.department, a.question.code, a.value, a.options.all(), a)
    # for se in survey.sections():
    #     for qu in se.questions():
    #         pass
