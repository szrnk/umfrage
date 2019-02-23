import tablib

from surveys.models import Answer, OPTION_CHOICES


def create_survey_output(survey):
    data = tablib.Dataset()
    for se in survey.sections():
        for qu in se.questions():
            if qu.qtype in OPTION_CHOICES:
                for op in qu.options().all():
                    data.append([se.code, qu.code, op.code, op.text])
            else:
                data.append([se.code, qu.code, 'V', '-'])
    data.headers = ['Section', 'Question', 'Op/Val', 'text']
    for inv in survey.invitation_set.all():
        col = []
        for se in survey.sections():
            for qu in se.questions():
                ans = Answer.objects.filter(department=inv.department, question_id=qu.id).first()
                if qu.qtype in OPTION_CHOICES:
                    for op in qu.options().all():
                        if se.triggered(inv.department):
                            if qu.triggered(inv.department) and ans:
                                o = ans.options.filter(id=op.pk).first()
                                col.append('*' if o is not None else '')
                            else:
                                col.append('')
                        else:
                            col.append('')
                elif ans is not None:
                    col.append(ans.value.text)
                else:
                    col.append('')
        data.append_col(col, header=inv.department.name)
    with open('temp.xls', 'wb') as f:
        f.write(data.xls)

    # print(data.export('xls'))

