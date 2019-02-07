from adminsortable2.admin import SortableInlineAdminMixin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.forms import Textarea
from django.urls import reverse
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter, \
    StackedPolymorphicInline, PolymorphicInlineSupportMixin

# https://stackoverflow.com/questions/14308050/django-admin-nested-inline
from django.utils.safestring import mark_safe

from .models import Survey, Section, Question, Option, Invitation, Answer, DisplayLogic, DisplayByOptions, DisplayByValue

FORMFIELD_OVERRIDES = {
    models.TextField: {
        "widget": Textarea(
            attrs={
                "rows": 5,
                # 'cols': 60,
                "class": "vLargeTextField",
            }
        )
    }
}


class EditLinkToParentSection(object):
    def section_edit_link(self, instance):
        if instance.pk:
            url = reverse(
                "admin:%s_%s_change"
                % (instance._meta.app_label, instance.section._meta.model_name),
                args=[instance.section.pk],
            )
            return mark_safe(u'<a href="{u}">edit parent section</a>'.format(u=url))
        else:
            return ""


class EditLinkToParentSurvey(object):
    def survey_edit_link(self, instance):
        if instance.pk:
            url = reverse(
                "admin:%s_%s_change"
                % (instance._meta.app_label, instance.survey._meta.model_name),
                args=[instance.survey.pk],
            )
            return mark_safe(u'<a href="{u}">edit parent survey</a>'.format(u=url))
        else:
            return ""


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        if instance.pk:
            model_name = instance._meta.model_name
            url = reverse(
                "admin:%s_%s_change" % (instance._meta.app_label, model_name),
                args=[instance.pk],
            )
            return mark_safe(
                u'<a href="{u}">edit {m} details</a>'.format(u=url, m=model_name)
            )
        else:
            return ""


class OptionAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES
    exclude = ("order", "question")


class DisplayLogicChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = DisplayLogic

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    # base_form = ...
    # base_fieldsets = (
    #     ...
    # )


class DisplayByOptionsAdmin(DisplayLogicChildAdmin):
    base_model = DisplayByOptions
    #show_in_index = True


class DisplayByValueAdmin(DisplayLogicChildAdmin):
    base_model = DisplayByValue
    #show_in_index = True


class DisplayLogicParentAdmin(PolymorphicParentModelAdmin):
    base_model = DisplayLogic  # Optional, explicitly set here.
    child_models = (DisplayByOptions, DisplayByValue, )


# class DisplayLogicInline(StackedPolymorphicInline):
#     """
#     An inline for a polymorphic model.
#     The actual form appearance of each row is determined by
#     the child inline that corresponds with the actual model type.
#     """
#     class DisplayByValueAdminInline(StackedPolymorphicInline.Child):
#         model = DisplayByValue
#
#     class DisplayByOptionAdminInline(StackedPolymorphicInline.Child):
#         model = DisplayByOptions
#
#     model = DisplayLogic
#     fk_name = 'shown_question'
#     child_inlines = (
#         DisplayByValueAdminInline,
#         DisplayByOptionAdminInline,
#     )


class OptionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Option
    formfield_overrides = FORMFIELD_OVERRIDES
    extra = 0


class QuestionAdmin(PolymorphicInlineSupportMixin, EditLinkToParentSection, admin.ModelAdmin):
    inlines = [OptionInline]
    formfield_overrides = FORMFIELD_OVERRIDES
    list_display = ("code", "truncated_text")
    # exclude = ('order', )
    readonly_fields = ("section", "section_edit_link")
    fieldsets = ((None, {"fields": ("section", "section_edit_link", "code", "text", "help_text", "qtype")}),)
    extra = 0


class QuestionInline(
    SortableInlineAdminMixin, EditLinkToInlineObject, admin.StackedInline
):
    model = Question
    extra = 0
    exclude = ("code",)
    readonly_fields = ("edit_link",)
    formfield_overrides = FORMFIELD_OVERRIDES


class SectionAdmin(EditLinkToParentSurvey, admin.ModelAdmin):
    inlines = [QuestionInline]
    formfield_overrides = FORMFIELD_OVERRIDES
    list_display = ("name",)
    readonly_fields = ("survey", "survey_edit_link")
    fieldsets = ((None, {"fields": ("survey", "survey_edit_link", "name", "title")}),)
    extra = 0


class SectionInline(
    SortableInlineAdminMixin, EditLinkToInlineObject, admin.StackedInline
):
    model = Section
    extra = 0
    exclude = ("code",)
    readonly_fields = ("edit_link",)
    formfield_overrides = FORMFIELD_OVERRIDES


class SurveyAdmin(admin.ModelAdmin):
    inlines = (SectionInline,)
    list_display = ("name",)
    extra = 0


def get_invitation_url(obj):
    return mark_safe(u'<a href="{u}">set as current survey</a>'.format(u=obj.get_url()))


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("department", "survey", get_invitation_url)
    extra = 0
    readonly_fields = (get_invitation_url,)


admin.site.register(Answer)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(DisplayLogic, DisplayLogicParentAdmin)
# admin.site.register(DisplayByOptions, DisplayByOptionsAdmin)
# admin.site.register(DisplayByValue, DisplayByValueAdmin)


# TODO: We want a better place to put these unregisters...
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
