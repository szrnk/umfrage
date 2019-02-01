from django.contrib.auth.signals import user_logged_in
from correspondents.models import Department
from surveys.models import Survey, Invitation


def capture_survey_and_department(sender, user, request, **kwargs):

    # department_id = request.session.get('department_id')
    # if department_id is not None:
    #     try:
    #         department = Department.objects.filter(id=department_id).first()
    #         if department is not None:
    #             user.department_id = department_id
    #             user.save()
    #     except Department.DoesNotExist:
    #         pass
    #
    # survey_id = request.session.get('survey_id')
    # if survey_id is not None:
    #     try:
    #         survey = Survey.objects.filter(id=survey_id).first()
    #         if survey is not None:
    #             user.surveys.add(survey)
    #             user.save()
    #     except Survey.DoesNotExist:
    #         pass

    invitation_token = request.session.get('invitation_token')
    if invitation_token is not None:
        try:
            invitation = Invitation.objects.filter(token=invitation_token).first()
            if invitation is not None:
                user.invitations.add(invitation)
                # user.save()
        except Invitation.DoesNotExist:
            pass


user_logged_in.connect(capture_survey_and_department)
