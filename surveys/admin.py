from adminsortable2.admin import SortableInlineAdminMixin
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from dal_select2.widgets import ModelSelect2, ModelSelect2Multiple
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.forms import Textarea, ModelForm, ModelChoiceField, CharField
from django.conf.urls import url
from django.urls import reverse

from polymorphic.admin import (PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
    StackedPolymorphicInline, PolymorphicInlineSupportMixin, )

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
                % (instance._meta.app_label, instance.parent_section._meta.model_name),
                args=[instance.parent_section.pk],
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


class DisplayByOptionForm(ModelForm):

    class Meta:
        model = DisplayByOptions
        fields = ('__all__')
        widgets = {
            'trigger_question': ModelSelect2(url='/surveys/trigger_questions', forward=['shown_element']),
            'options': ModelSelect2Multiple(url='/surveys/linked_options', forward=['trigger_question'])
        }

    class Media:
        js = (
            'linked_data.js',
        )


class DisplayByValueForm(ModelForm):

    class Meta:
        model = DisplayByValue
        fields = ('__all__')
        widgets = {
            'trigger_question': ModelSelect2(url='/surveys/trigger_questions', forward=['shown_element']),
        }

    class Media:
        js = (
            'linked_data.js',
        )


class DisplayByOptionsAdmin(DisplayLogicChildAdmin):
    base_model = DisplayByOptions
    form = DisplayByOptionForm


class DisplayByValueAdmin(DisplayLogicChildAdmin):
    base_model = DisplayByValue
    form = DisplayByValueForm


class DisplayLogicParentAdmin(PolymorphicParentModelAdmin):
    base_model = DisplayLogic  # Optional, explicitly set here.
    child_models = (DisplayByOptions, DisplayByValue, )


class DisplayLogicInline(StackedPolymorphicInline):
    """
    An inline for a polymorphic model.
    The actual form appearance of each row is determined by
    the child inline that corresponds with the actual model type.
    """
    verbose_name_plural = 'Display Conditions'
    verbose_name = 'Display Condition'

    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        if self.parent_model == Question:
            self.verbose_name_plural = self.verbose_name_plural + ' for this Question'
            self.verbose_name = self.verbose_name + ' for this Question'
        if self.parent_model == Section:
            self.verbose_name_plural = self.verbose_name_plural + ' for this Section'
            self.verbose_name = self.verbose_name + ' for this Section'

    class DisplayByValueAdminInline(StackedPolymorphicInline.Child):
        model = DisplayByValue
        form = DisplayByValueForm

    class DisplayByOptionAdminInline(StackedPolymorphicInline.Child):
        model = DisplayByOptions
        form = DisplayByOptionForm

        class Meta:
            model = DisplayByOptions
            fields = ('trigger_question', 'options')

        class Media:
            js = (
                'linked_data.js',
            )

    model = DisplayLogic
    fk_name = 'shown_element'
    child_inlines = (
        DisplayByValueAdminInline,
        DisplayByOptionAdminInline,
    )


class OptionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Option
    formfield_overrides = FORMFIELD_OVERRIDES
    extra = 0


class QuestionAdmin(EditLinkToParentSection, PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [OptionInline, DisplayLogicInline]
    formfield_overrides = FORMFIELD_OVERRIDES
    list_display = ("code", "truncated_text")
    readonly_fields = ("parent_section", "section_edit_link")
    fieldsets = ((None, {"fields": ("parent_section", "section_edit_link", "code", "text", "help_text", "qtype")}),)
    extra = 0


class QuestionInline(
    SortableInlineAdminMixin, EditLinkToInlineObject, admin.StackedInline
):
    model = Question
    fk_name = "parent_section"
    extra = 0
    exclude = ("code",)
    readonly_fields = ("edit_link",)
    formfield_overrides = FORMFIELD_OVERRIDES


class SectionAdmin(EditLinkToParentSurvey, PolymorphicInlineSupportMixin, admin.ModelAdmin):
    inlines = [QuestionInline, DisplayLogicInline]
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
admin.site.register(DisplayByOptions, DisplayByOptionsAdmin)
admin.site.register(DisplayByValue, DisplayByValueAdmin)


# TODO: We want a better place to put these unregisters...
admin.site.unregister(Group)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
