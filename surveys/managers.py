from django.db import models


class QuestionQuerySet(models.QuerySet):

    def answered_by_department(self, department=None):
        assert department is not None
        return self.filter(department_id=department.pk)
