from .models import Survey


class Progress(object):
    """
    Maintains session based tracking for section and question, per survey.
    All keys must be str type.

    """

    def __init__(self, request, survey):
        self.sections = survey.sections()
        self.survey_key = str(survey.id)
        self.initialize_progress_in_session(request, survey)
        self.current_section = self.sections[
            self.progress[self.survey_key]["section_index"]
        ]
        # self.progress = None

    def is_last_section(self):
        return self.progress[self.survey_key]["section_index"] + 1 >= len(self.sections)

    def is_end_of_section(self):
        return (
            self.progress[self.survey_key]["question_index"] + 1
            >= self.current_section.question_set.count()
        )

    def advance(self, request):
        """
        move to the next question and or section.
        :return:
        """
        if self.is_end_of_section():
            if self.is_last_section():
                return None  # meaning we are done
            else:
                self.progress[self.survey_key]["section_index"] += 1
                self.progress[self.survey_key]["question_index"] = 0
        else:
            self.progress[self.survey_key]["question_index"] += 1
        self.save(request)

    def save(self, request):
        request.session["progress"] = self.progress
        pass

    def get_data(self):
        return self.progress

    def initialize_progress_in_session(self, request, survey):
        """
        session['progress'] = {'<SID>': {'section_index':0, 'question_index':0}}
        Where '<SID>' is the str(survey.id). We allow multiple surveys to be managed

        :param request:
        :param survey:
        :return:  the progress dict for the survey in question
        """

        write = False

        # get/build
        progress = request.session.get("progress")
        if progress is None:
            progress = dict()
            write = True

        if self.survey_key not in progress:
            progress[self.survey_key] = dict(section_index=0, question_index=0)
            write = True

        # ensure all fields present, in case we had a partial session in place
        if not progress[self.survey_key].get("section_index"):
            progress[self.survey_key]["section_index"] = 0
            write = True
        if not progress[self.survey_key].get("question_index"):
            progress[self.survey_key]["question_index"] = 0
            write = True

        self.progress = progress

        if write:
            self.save(request)
