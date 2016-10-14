from django.conf import settings
from django.template import Template, Context

import json


class FakeRequest(object):
    def __init__(self):
        self.base = settings.EXTERNAL_URL
        if self.base.endswith('/'):
            self.base = self.base[:-1]

    def build_absolute_uri(self, location):
        return "{}{}".format(self.base, location)

request = FakeRequest()


class NotificationMethod(object):
    name = 'method_template'
    verbose_name = 'Notification method template'
    use_subject = False
    use_short_description = False
    use_description = False
    options = {}

    def __init__(self):
        self.server_configured = False

    def enabled(self, event, user, paths):
        from fir_async.models import NotificationPreference
        try:
            preference = NotificationPreference.objects.get(event=event, method=self.name, user=user)
        except NotificationPreference.DoesNotExist:
            return False
        for bl in preference.business_lines.all():
            if any([bl.path.startswith(path) for path in paths]):
                return True
        return False

    @staticmethod
    def prepare(template_object, instance, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context.update({'instance': instance})
        context = Context(extra_context)
        return {
            'subject': Template(getattr(template_object, 'subject', "")).render(context),
            'short_description': Template(getattr(template_object, 'short_description', "")).render(context),
            'description': Template(getattr(template_object, 'description', "")).render(context)
        }

    def _get_template(self, templates):
        for template in templates:
            if self.use_subject and template.subject is None:
                continue
            if self.use_short_description and template.short_description is None:
                continue
            if self.use_description and template.description is None:
                continue
            return template
        return None

    def _get_configuration(self, user):
        from fir_async.models import MethodConfiguration
        try:
            string_config = MethodConfiguration.objects.get(user=user, key=self.name).value
        except MethodConfiguration.DoesNotExist:
            return {}
        try:
            return json.loads(string_config)
        except:
            return {}

    def send(self, event, users, instance, paths):
        raise NotImplementedError

    def configured(self, user):
        return self.server_configured and user.is_active

    def form(self, *args, **kwargs):
        from fir_async.forms import MethodConfigurationForm
        if not len(self.options):
            return None
        user = kwargs.pop('user', None)
        if user is not None:
            kwargs['initial'] = self._get_configuration(user)
            kwargs['user'] = user
        kwargs['method'] = self
        return MethodConfigurationForm(*args, **kwargs)
