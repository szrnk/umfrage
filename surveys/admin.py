from adminsortable2.admin import SortableInlineAdminMixin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from .models import Survey, Question, Option


class OptionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Option
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        OptionInline,
    ]
    list_display = ('code', 'truncated_text', 'number_of_options')
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]
    list_display = ('name', 'number_of_questions')
    extra = 0


admin.site.register(Option)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Survey, SurveyAdmin)

# TODO: We want a better place to put these...
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
