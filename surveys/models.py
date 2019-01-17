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
        return self.question_set.all();

    def number_of_questions(self):
        return len(self.questions())


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def options(self):
        return self.option_set.all()

    def number_of_options(self):
        return len(self.options())

    def truncated_text(self):
        return self.text[:30]

    class Meta:
        # order must be first
        ordering = ["order"]

    def __str__(self):
        return self.text[:40]


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

