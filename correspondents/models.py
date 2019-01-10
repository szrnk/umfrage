from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    email = models.EmailField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    contact_name = models.CharField(max_length=50)
    contact_email = models.EmailField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


