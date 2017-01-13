from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from incidents.models import model_created, Incident, model_updated

from fir_async.registry import registry, async_event


@python_2_unicode_compatible
class MethodConfiguration(models.Model):
    user = models.ForeignKey('auth.User', related_name='method_preferences', verbose_name=_('user'))
    key = models.CharField(max_length=60, choices=registry.get_method_choices(), verbose_name=_('method'))
    value = models.TextField(verbose_name=_('configuration'))

    def __str__(self):
        return "{user}: {method} configuration".format(user=self.user, method=self.key)

    class Meta:
        verbose_name = _('method configuration')
        verbose_name_plural = _('method configurations')
        unique_together = (("user", "key"),)
        index_together = ["user", "key"]


class NotificationTemplate(models.Model):
    event = models.CharField(max_length=60, choices=registry.get_event_choices(), verbose_name=_('event'))
    business_lines = models.ManyToManyField('incidents.BusinessLine', related_name='+', blank=True,
                                            verbose_name=_('business line'))
    subject = models.CharField(max_length=200, blank=True, default="", verbose_name=_('subject'))
    short_description = models.TextField(blank=True, default="", verbose_name=_('short description'))
    description = models.TextField(blank=True, default="", verbose_name=_('description'))

    class Meta:
        verbose_name = _('notification template')
        verbose_name_plural = _('notification templates')


@python_2_unicode_compatible
class NotificationPreference(models.Model):
    user = models.ForeignKey('auth.User', related_name='notification_preferences', verbose_name=_('user'))
    event = models.CharField(max_length=60, verbose_name=_('event'))
    method = models.CharField(max_length=60, verbose_name=_('method'))
    business_lines = models.ManyToManyField('incidents.BusinessLine', related_name='+', blank=True,
                                            verbose_name=_('business lines'))

    def __str__(self):
        return "{user}: {event} notification preference for {method}".format(user=self.user,
                                                                               event=self.event,
                                                                               method=self.method)

    class Meta:
        verbose_name = _('notification preference')
        verbose_name_plural = _('notification preferences')
        unique_together = (("user", "event", "method"),)
        index_together = ["user", "event", "method"]


@async_event('event:created', model_created, Incident, verbose_name='Event created')
def incident_created(sender, instance, **kwargs):
    return instance, instance.concerned_business_lines


@async_event('event:updated', model_updated, Incident, verbose_name='Event updated')
def incident_created(sender, instance, **kwargs):
    return instance, instance.concerned_business_lines

