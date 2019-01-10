from django.contrib import admin

from .models import Hospital, Department


class DepartmentInline(admin.StackedInline):
    model = Department
    fieldsets = (
        (None, {
            'fields': (('name',),  ('contact_name', 'contact_phone', 'contact_email'), ('address', 'address_detail'),
                       ('city', 'state_province', 'country'),
                       ('website',),
                       )
        }),
    )
    extra = 1


class HospitalAdmin(admin.ModelAdmin):
    inlines = [
        DepartmentInline,
    ]
    list_display = ('name', 'city', 'state_province')
    fieldsets = (
        (None, {
            'fields': (('name', 'phone', 'email'), ('address', 'address_detail'), ('city', 'state_province', 'country'), ('website',))
        }),
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': ('registration_required', 'template_name'),
        # }),
    )
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'city', 'state_province')
    fieldsets = (
        (None, {
            'fields': (('name', 'hospital'), ('contact_name', 'contact_phone', 'contact_email'), ('address', 'address_detail'),
                       ('city', 'state_province', 'country'),
                       ('website',),
                       )
        }),
    )


admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Department, DepartmentAdmin)
