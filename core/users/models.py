from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .signals import capture_survey_and_department


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    department = models.ForeignKey("correspondents.Department", on_delete=models.CASCADE, null=True)
    surveys = models.ManyToManyField("surveys.Survey")
    invitations = models.ManyToManyField("surveys.Invitation")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

