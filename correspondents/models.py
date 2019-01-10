from django.db import models
from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Hospital(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=30)
    address_detail = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=30)
    state_province = models.CharField(max_length=25)
    country = models.CharField(max_length=45)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=30)
    address_detail = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=30)
    state_province = models.CharField(max_length=25)
    country = models.CharField(max_length=45)
    website = models.URLField(blank=True)
    contact_name = models.CharField(max_length=40, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


