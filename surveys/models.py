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


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    text = models.TextField()

    def options(self):
        return Option.objects.filter(question_id=self.pk)

    class Meta:
        ordering = ["-code"]

    def __str__(self):
        return self.text[:20]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    text = models.TextField()

    class Meta:
        ordering = ["-code"]

    def __str__(self):
        return self.text[:20]

