from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=30)
    # address = models.CharField(max_length=50)
    # city = models.CharField(max_length=60)
    # state_province = models.CharField(max_length=30)
    # country = models.CharField(max_length=50)
    # website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def questions(self):
        return Question.objects.filter(survey_id=self.pk)

    def number_of_questions(self):
        return len(self.questions())


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def options(self):
        return Option.objects.filter(question_id=self.pk)

    def number_of_options(self):
        return len(self.options())

    def truncated_text(self):
        return self.text[:30]

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return self.text[:20]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return self.text[:20]

