from django import forms
from django.contrib import admin
from django.conf import settings
from fir_async.registry import registry
from fir_plugins.admin import MarkdownModelAdmin
from fir_async.models import MethodConfiguration, NotificationTemplate, NotificationPreference


class NotificationTemplateForm(forms.ModelForm):
    event = forms.ChoiceField(choices=registry.get_event_choices())

    class Meta:
        fields = '__all__'


class NotificationTemplateAdmin(MarkdownModelAdmin):
    markdown_fields = ('description', 'short_description')
    form = NotificationTemplateForm


admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
if settings.DEBUG:
    admin.site.register(NotificationPreference)
    admin.site.register(MethodConfiguration)
