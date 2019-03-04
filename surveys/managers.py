from django.db import models
from polymorphic.managers import PolymorphicManager


class QuestionQuerySet(PolymorphicManager):
    def answered_by_department(self, department=None):
        assert department is not None
        return self.filter(department_id=department.pk)
