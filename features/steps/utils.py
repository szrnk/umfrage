from factory.django import DjangoModelFactory


class HospitalFactory(DjangoModelFactory):
    class Meta:
        model = 'correspondents.Hospital'
        django_get_or_create = ('name',)

    name = 'H1'


class DepartmentFactory(DjangoModelFactory):
    class Meta:
        model = 'correspondents.Department'
        django_get_or_create = ('name',)

    name = 'D1'
