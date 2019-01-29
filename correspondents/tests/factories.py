from factory import DjangoModelFactory, Sequence, SubFactory

from ..models import Hospital, Department


class HospitalFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Hospital %03d" % n)

    class Meta:
        model = Hospital


class DepartmentFactory(DjangoModelFactory):
    hospital = SubFactory(HospitalFactory)
    name = Sequence(lambda n: "Department %03d" % n)

    class Meta:
        model = Department


def basic_hospital_structure(hospital_name=None, department_name=None):

    # allow a one-shot hospital name
    if hospital_name is not None:
        hospital_kwargs = dict(name=hospital_name)
    else:
        hospital_kwargs = dict()

    # allow a one-shot department name
    if department_name is not None:
        department_kwargs = dict(name=department_name)
    else:
        department_kwargs = dict()

    hospitals = []
    for hoi in range(2):
        ho = HospitalFactory(**hospital_kwargs)
        hospital_kwargs = dict()
        for dei in range(4):
            de = DepartmentFactory(hospital=ho, **department_kwargs)
            department_kwargs = dict()
        hospitals.append(ho)
    return hospitals


