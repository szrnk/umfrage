from adminsortable2.admin import SortableInlineAdminMixin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.forms import Textarea
from django.urls import reverse
# https://stackoverflow.com/questions/14308050/django-admin-nested-inline
from django.utils.safestring import mark_safe

from .models import Survey, Question, Option

FORMFIELD_OVERRIDES = {
    models.TextField: {'widget': Textarea(
        attrs={'rows': 6,
               # 'cols': 60,
               'class': 'vLargeTextField',
               })},
}


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        if instance.pk:
            url = reverse('admin:%s_%s_change' % (
                instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
            return mark_safe(u'<a href="{u}">edit details</a>'.format(u=url))
        else:
            return ''


class OptionAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES
    exclude = ('order', 'question')


class OptionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Option
    formfield_overrides = FORMFIELD_OVERRIDES
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]
    formfield_overrides = FORMFIELD_OVERRIDES
    list_display = ('code', 'truncated_text', 'number_of_options')
    exclude = ('order', )
    readonly_fields = ('survey', )
    fieldsets = (
        (None, {
            'fields': ('survey', 'code', 'text',)
        }),)
    extra = 0


class QuestionInline(SortableInlineAdminMixin, EditLinkToInlineObject, admin.StackedInline):
    model = Question
    extra = 0
    readonly_fields = ('edit_link', )
    fieldsets = (
        (None, {
            'fields': (('edit_link',), ('text',))
        }),)
    formfield_overrides = FORMFIELD_OVERRIDES


class SurveyAdmin(admin.ModelAdmin):
    inlines = (QuestionInline, )
    list_display = ('name', 'number_of_questions')
    extra = 0


admin.site.register(Option, OptionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Survey, SurveyAdmin)

# TODO: We want a better place to put these...
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
