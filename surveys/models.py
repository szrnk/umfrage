from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import Truncator
from polymorphic.models import PolymorphicModel

from correspondents.models import Department
from .managers import QuestionQuerySet


class Survey(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def sections(self):
        return self.section_set.all()


class Element(PolymorphicModel):

    def __str__(self):
        return f"E: {self.id}"


class Section(Element):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    # Name is for the survey developer only
    name = models.CharField(max_length=100)
    # Title is used on frontend - and to be internationalised
    title = models.CharField(max_length=100, blank=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return self.name

    def questions(self):
        return self.question_set.all()

    def number_of_questions(self):
        return len(self.questions())


TYPE_CHOICES = (("SINGLECHOICE", "Radio"), ("MULTICHOICE", "Checkboxes"), ("SELECT", "Select (Dropdown)"), ("TEXT", "Text"),
                ("ESSAY", "Essay"), ("INTEGER", "Integer"), ("EMAIL", "Email"),)


class Question(Element):
    parent_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    text = models.TextField(blank=True)
    help_text = models.TextField(blank=True)
    qtype = models.CharField(max_length=20, choices=TYPE_CHOICES, default="SINGLECHOICE")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    objects = QuestionQuerySet()

    def options(self):
        return self.option_set.all()

    def number_of_options(self):
        return len(self.options())

    def truncated_text(self):
        return Truncator(self.text).chars(30)

    def triggered(self):
        # There are no dependencies, so trigger
        if not self.trigger_questions.all().count():
            return True
        # Trigger if there are any dependencies that match
        return any(q.show() for q in self.trigger_questions.all())

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return f'Q: {self.truncated_text()}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return f'Su:{self.question.section.survey.id} Se: {self.question.section.id} Q:{self.question.id} O:{self.id} ' + Truncator(self.text).chars(20)


class Value(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.ManyToManyField(Option)
    value = models.OneToOneField(Value, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(
        "correspondents.Department", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<Answer {self.id}>"

    # def __repr__(self):
    #     return f"<Answer {self.pk}> option:{self.option} for {self.question} for {self.department}"


def generate_random_token():
    return get_random_string(length=32)


class Invitation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default=generate_random_token)

    def __str__(self):
        return f"Invited {self.department.name} to {self.survey.name}"

    def get_url(self):
        return reverse("surveys:invite", kwargs={"token": self.token})


def NON_POLYMORPHIC_CASCADE(collector, field, sub_objs, using):
    return models.CASCADE(collector, field, sub_objs.non_polymorphic(), using)


class DisplayLogic(PolymorphicModel):
    shown_element = models.ForeignKey('Element', related_name='trigger_questions', null=True,
                                       on_delete=NON_POLYMORPHIC_CASCADE)
    trigger_question = models.ForeignKey('Question',  related_name='shown_element', null=True,
                                         on_delete=NON_POLYMORPHIC_CASCADE)

    def __str__(self):
        return f"DiLog {self.trigger_question.id} triggers {self.shown_element.id}"


class DisplayByOptions(DisplayLogic):

    options = models.ManyToManyField(Option)

    def show(self):
        if self.trigger_question.answer_set.count() == 0:
            return False
        intersection = self.trigger_question.answer_set.first().options.all().order_by().intersection(self.options.order_by().all())
        return intersection.count()


SHOW_LOGIC_CHOICES = (("==", "=="), (">=", ">="), ("<=", "<="), ("contains", "contains"), ("containsNoCase", "containsNoCase"), )


class DisplayByValue(DisplayLogic):
    value = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=SHOW_LOGIC_CHOICES, default="==")

    def show(self):
        if self.trigger_question.answer_set.count() == 0:
            return False

        avalue = self.trigger_question.answer_set.first().value.text

        if self.condition == '==':
            if avalue == self.value:
                return True
        elif self.condition == '>=':
            if int(avalue) >= int(self.value):
                return True
        elif self.condition == '<=':
            if int(avalue) <= int(self.value):
                return True
        elif self.condition == 'contains':
            if self.value in avalue:
                return True
        elif self.condition == 'containsNoCase':
            if self.value.lower() in avalue.lower():
                return True
        return False




