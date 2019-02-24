import tablib
from pyquery import PyQuery as pq

from surveys.models import Answer, OPTION_CHOICES


def embellish_table(raw):
    h = pq(raw)
    h('table').add_class('table-header-rotated')
    for i, el in enumerate(h('thead').find('th')):
        if i < 4:
            continue
        text = el.text
        new_h = pq(f'<th class="rotate"><div><span>{text}</span></div></th>')
        pq(el).replace_with(new_h)
    h('thead').find('th').attr.scope = 'col'
    h('tbody').find('th').add_class('row-header')
    h('tbody').find('th').attr.scope = 'row'
    return str(h)


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
        inst = ', '.join((inv.department.name, inv.department.hospital.name, inv.department.hospital.city))
        data.append_col(col, header=inst)
    return data


def create_survey_html_output(survey):
    data = create_survey_output(survey)
    return embellish_table(data.html)


def create_survey_csv(survey):
    data = create_survey_output(survey)
    return data.csv
    # with open('temp.csv', 'wb') as f:
    #     f.write(data.csv)
