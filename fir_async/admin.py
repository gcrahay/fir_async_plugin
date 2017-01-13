from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

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
    list_display = ('event', 'business_lines_list')

    def business_lines_list(self, obj):
        bls = obj.business_lines.all()
        if bls.count():
            return ', '.join([bl.name for bl in bls])
        return pgettext_lazy('business lines', 'All')
    business_lines_list.short_description = _('Business lines')


admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
if settings.DEBUG:
    admin.site.register(NotificationPreference)
    admin.site.register(MethodConfiguration)
