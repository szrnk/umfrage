from django.contrib import admin

from .models import Hospital, Department


class DepartmentInline(admin.StackedInline):
    model = Department


class HospitalAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentInline,
    ]
    list_display = ('name', 'city', 'state_province')


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Department)
