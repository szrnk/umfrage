from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import Truncator

from correspondents.models import Department
from .managers import QuestionQuerySet


class Survey(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def sections(self):
        return self.section_set.all()


class Section(models.Model):
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
                ("ESSAY", "Essay"))


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    text = models.TextField(blank=True)
    help_text = models.TextField(blank=True)
    qtype = models.CharField(max_length=20, choices=TYPE_CHOICES, default="SINGLECHOICE")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = QuestionQuerySet.as_manager()

    def options(self):
        return self.option_set.all()

    def number_of_options(self):
        return len(self.options())

    def truncated_text(self):
        return Truncator(self.text).chars(30)

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return self.truncated_text()


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return Truncator(self.text).chars(20)


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
